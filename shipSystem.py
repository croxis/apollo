import sandbox

from direct.stdpy.file import *

from panda3d.bullet import BulletDebugNode, BulletRigidBodyNode, BulletSphereShape
from panda3d.core import Point3, Vec3

import graphicsComponents
import physics
import shipComponents
import solarSystem
import universals

import glob
import re
import yaml

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "notify-level-ITF-ShipSystem debug")
from direct.directnotify.DirectNotify import DirectNotify
log = DirectNotify().newCategory("ITF-ShipSystem")


class ShipSystem(sandbox.EntitySystem):
    def init(self):
        self.accept("setPlayerStations", self.setPlayerStation)
        self.accept("setShipID", self.setShipID)
        self.accept('shipClassList', self.checkClasses)
        self.accept('shipUpdate', self.shipUpdate)
        self.accept('shipUpdates', self.shipUpdates)
        self.accept('playerDisconnected', self.playerDisconnected)
        self.shipClasses = {}
        self.shipid = None  # This is for clients to id who the controlling
        # ship is for quick lookup

    def process(self, entity):
        pass

    def setShipID(self, data):
        self.shipid = data.id

    def checkClasses(self, shipClasses):
        for ship in shipClasses.shipClass:
            if ship.className not in self.shipClasses:
                import sys
                sandbox.log.warning("Ship type " + ship.folder + ' does not exist!')
                sandbox.log.warning("Current DB: " + str(self.shipClasses))
                sys.exit(1)

    def loadShipClasses(self):
        shippaths = glob.glob('ships/*/ship.yaml')
        for yamlPath in shippaths:
            shipFile = open(yamlPath)
            ship = yaml.load(shipFile)

            re1 = '.*?'   # Non-greedy match on filler
            re2 = '(?:[a-z][a-z]+)'   # Uninteresting: word
            re3 = '.*?'   # Non-greedy match on filler
            re4 = '((?:[a-z][a-z]+))'  # Word 1

            rg = re.compile(re1 + re2 + re3 + re4, re.IGNORECASE | re.DOTALL)
            m = rg.search(yamlPath)

            #ship['path'] = 'ships/' + ship['mesh'] + '/'
            ship['path'] = m.group(1) + '/' + ship['mesh']
            ship['folder'] = m.group(1)
            shipFile.close()
            #TODO switch class name to folder name
            self.shipClasses[ship['class']] = ship
            universals.log.info("Loaded " + ship['mesh'])

    def shipUpdate(self, ship, playerShip=False):
        if ship.id not in sandbox.entities:
            self.spawnShip(ship.name, ship.className, playerShip=False, entityid=ship.id)
            #TODO: Request for full info from server and just return if no name or class?
        physicsComponent = sandbox.entities[ship.id].getComponent(shipComponents.BulletPhysicsComponent)
        physicsComponent.nodePath.setPos(ship.x, ship.y, 0)
        physicsComponent.nodePath.setHpr(ship.h, 0, 0)
        physicsComponent.node.setLinearVelocity((ship.dx, ship.dy, 0))
        physicsComponent.node.setAngularVelocity((ship.dh, 0, 0))
        physicsComponent.currentThrust = ship.thrust
        physicsComponent.currentTorque = ship.torque

    def shipUpdates(self, ships):
        for ship in ships.ship:
            self.shipUpdate(ship)

    def spawnShip(self, shipName, shipClass, playerShip=False, entityid=-1):
        if shipName == '' or shipClass == '':
            return
        if entityid == -1:
            ship = sandbox.createEntity()
        else:
            ship = sandbox.addEntity(entityid)
        if playerShip:
            component = shipComponents.PlayerComponent()
            ship.addComponent(component)
        component = shipComponents.BulletPhysicsComponent()
        component.bulletShape = BulletSphereShape(5)
        component.node = BulletRigidBodyNode(shipName)
        component.node.setMass(self.shipClasses[shipClass]['mass'])
        component.node.addShape(component.bulletShape)
        component.debugNode = BulletDebugNode(shipName + "_debug")
        component.debugNode.showWireframe(True)
        component.debugNode.showConstraints(True)
        component.debugNode.showBoundingBoxes(True)
        component.debugNode.showNormals(True)
        component.debugNodePath = sandbox.base.render.attachNewNode(component.debugNode)
        component.debugNodePath.show()
        component.nodePath = universals.solarSystemRoot.attachNewNode(component.node)
        component.currentSOI = universals.defaultSOIid
        #physics.addBody(component.node)
        if playerShip:
            earth = universals.solarSystemRoot.find('**/Earth')
            #ePos = sandbox.getSystem(solarSystem.SolarSystemSystem).get2DBodyPosition(earth, universals.day)
            ePos = earth.getPos()
            spawn = ePos + Point3(6771, 0, 0)
            #spawn = Point3(6771, 0, 0)
            print "Spawn", spawn
            velocity = Vec3(0, 7.67254, 0)
            component.nodePath.setPos(spawn)
            component.node.setLinearVelocity(velocity)
        physics.addBody(component.node)
        #position = sandbox.getSystem(solarSystem.SolarSystemSystem).solarSystemRoot.find("**/Earth").getPos()
        #component.nodePath.setPos(position + Point3(6671, 0, 0))
        #component.node.setLinearVelocity(Vec3(0, 7.72983, 0))
        ship.addComponent(component)
        component = shipComponents.ThrustComponent()
        for engine in self.shipClasses[shipClass]['engines']:
            component.forward += engine['thrust']
        component.heading = self.shipClasses[shipClass]['torque']
        ship.addComponent(component)
        component = shipComponents.InfoComponent()
        component.shipClass = shipClass
        component.name = shipName
        ship.addComponent(component)
        if universals.runClient:
            component = graphicsComponents.RenderComponent()
            component.mesh = sandbox.base.loader.loadModel('ships/' + self.shipClasses[shipClass]['path'])
            component.mesh.reparentTo(sandbox.base.render)
            component.mesh.setScale(0.001)
            ship.addComponent(component)
        sandbox.send("shipGenerated", [ship])
        log.info("Ship spawned: " + shipName + " " + shipClass)
        #TODO Transmit player's ship data
        #TODO Broadcast new ship data
        #TODO Prioritize updating new client of surroundings

    def getPlayerShipEntities(self):
        return sandbox.getEntitiesByComponentType(shipComponents.PlayerComponent)

    def setPlayerStation(self, netAddress, shipid, stations):
        entity = sandbox.entities[shipid]
        playerComponent = entity.getComponent(shipComponents.PlayerComponent)
        acceptedStations = []
        for stationName in universals.playerStations:
            if getattr(playerComponent, stationName) == 0 and hasattr(stations, stationName):
                if getattr(stations, stationName) == 1:
                    setattr(playerComponent, stationName, netAddress)
                    acceptedStations.append(stationName)
        sandbox.send("confirmPlayerStations", [netAddress, shipid, acceptedStations])

    def playerDisconnected(self, address):
        ships = self.getPlayerShipEntities()
        for ship in ships:
            playerComponent = sandbox.entities[ship.id].getComponent(shipComponents.PlayerComponent)
            for stationName in universals.playerStations:
                if getattr(playerComponent, stationName) == address:
                    setattr(playerComponent, stationName, 0)
                    sandbox.send('stationEmptied', [shipid, stationName])
