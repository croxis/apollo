import sandbox

from direct.stdpy.file import *

from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape
from panda3d.core import Point3, Vec3

import graphics
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

    def spawnShip(self, shipName, shipClass, playerShip=False, entityid=-1):
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
        component.nodePath = universals.solarSystemRoot.attachNewNode(component.node)
        physics.addBody(component.node)
        position = sandbox.getSystem(solarSystem.SolarSystemSystem).solarSystemRoot.find("**/Earth").getPos()
        component.nodePath.setPos(position + Point3(6671, 0, 0))
        component.node.setLinearVelocity(Vec3(0, 7.72983, 0))
        ship.addComponent(component)
        component = shipComponents.ThrustComponent()
        ship.addComponent(component)
        component = shipComponents.InfoComponent()
        component.shipClass = shipClass
        component.name = shipName
        ship.addComponent(component)
        if universals.runClient:
            component = graphics.RenderComponent()
            component.mesh = sandbox.base.loader.loadModel('ships/' + self.shipClasses[shipClass]['path'])
            component.mesh.reparentTo(sandbox.base.render)
        sandbox.send("shipGenerated", [ship])
        log.info("Ship spawned: " + shipName + " " + shipClass)
        #messenger.send("putPlayerOnShip", [accountEntity.id, ship.id])
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
        shipids = self.getPlayerShipEntities()
        for shipid in shipids:
            playerComponent = sandbox.entities[shipid].getComponent(shipComponents.PlayerComponent)
            for stationName in universals.playerStations:
                if getattr(playerComponent, stationName) == address:
                    setattr(playerComponent, stationName, 0)
                    sandbox.send('stationEmptied', [shipid, stationName])
