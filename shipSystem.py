import sandbox

from direct.actor.Actor import Actor
from direct.interval.LerpInterval import LerpHprInterval
from direct.stdpy.file import *

from panda3d.bullet import BulletDebugNode, BulletRigidBodyNode, BulletSphereShape
from panda3d.core import LPoint3d, NodePath, Vec3

import graphicsComponents
import physics
import shipComponents
import universals

import glob
import re
import yaml

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "notify-level-ITF-ShipSystem debug")
from direct.directnotify.DirectNotify import DirectNotify
log = DirectNotify().newCategory("ITF-ShipSystem")


#Conversion factor from SI to units used in game
CONVERT = 1000.0


class ShipSystem(sandbox.EntitySystem):
    def init(self):
        self.accept("setPlayerStations", self.setPlayerStation)
        self.accept("setShipID", self.setShipID)
        self.accept('shipClassList', self.checkClasses)
        self.accept('shipUpdate', self.shipUpdate)
        self.accept('shipUpdates', self.shipUpdates)
        self.accept('spawnShip', self.spawnShip)
        self.accept('setTarget', self.setTarget)
        self.accept('playerDisconnected', self.playerDisconnected)
        self.shipClasses = {}
        self.shipid = None  # This is for clients to id who the controlling
        # ship is for quick lookup
        sandbox.ships = NodePath("ships")
        sandbox.ships.reparentTo(sandbox.base.render)

    def process(self, entity):
        #TODO: Turret tracking here
        # Turret tracking done here
        mesh = entity.getComponent(graphicsComponents.RenderComponent).mesh
        turrets = entity.getComponent(shipComponents.TurretsComponent)
        for turretEntity in turrets:
            turret = turretEntity.getComponent(shipComponents.TurretComponent)
            #target = sandbox.entities[turret.targetID].getComponent(shipComponents.BulletPhysicsComponent)
            targetRender = sandbox.entities[turret.targetID].getComponent(graphicsComponents.RenderComponent)
            traverser = mesh.controlJoint(None, 'modelRoot', (turret.name + ' traverser').replace(' ', '-'))
            hpr = mesh.getHpr(targetRender.mesh)

            shipClass = self.shipClasses[entity.getComponent(shipComponents.InfoComponent).shipClass]
            rotationSpeed = shipClass['weapons'][turret.name]['rotationSpeed']
            deltaH = (360 / float(rotationSpeed)) * globalClock.getDt()

            directionDistance =\
                sandbox.mathextra.signedAngularDistance(
                    hpr[0],
                    traverser.getH()
                )

            if directionDistance > 0.1:
                traverser.setH(traverser.setH(traverser.getH + deltaH))
            elif directionDistance < -0.1:
                traverser.setH(traverser.setH(traverser.getH - deltaH))

    def setTarget(self, masterShipID, data):
        # TODO: Support client sending specific turrets
        # Get ship turrets
        allTurrets = sandbox.getEntitiesByComponentType(shipComponents.TurretComponent)
        turrets = []
        for turret in allTurrets:
            if turret.getComponent(shipComponents.TurretComponent).parentID == masterShipID:
                if data.turretId == -1:
                    turrets.append(turret.getComponent(shipComponents.TurretComponent))
                elif data.turretId == turrent.id:
                    turrets.append(turret.getComponent(shipComponents.TurretComponent))
        for turret in turrets:
            turret.targetID = data.targetId

    def setShipID(self, data):
        self.shipid = data.id
        universals.shipid = data.id

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
            #self.spawnShip(ship.name, ship.className, playerShip, entityid=ship.id)
            self.spawnShip(ship.name, ship.className, playerShip=True, entityid=ship.id, turrets=ship.turrets)
            sandbox.send('updateStationGUI')
            #TODO: Request for full info from server and just return if no name or class?
        physicsComponent = sandbox.entities[ship.id].getComponent(shipComponents.BulletPhysicsComponent)
        physicsComponent.setTruePos(ship.x, ship.y)
        physicsComponent.nodePath.setHpr(ship.h, 0, 0)
        physicsComponent.node.setLinearVelocity((ship.dx, ship.dy, 0))
        physicsComponent.node.setAngularVelocity((0, 0, ship.dh))
        physicsComponent.currentThrust = ship.thrust
        physicsComponent.currentTorque = ship.torque

    def shipUpdates(self, ships):
        for ship in ships.ship:
            self.shipUpdate(ship)

    def spawnShip(
        self, shipName, shipClass, spawnPoint=LPoint3d(0, 0, 0),
        playerShip=False, entityid=-1, turrets=None
    ):
        if shipName == '' or shipClass == '':
            return
        if entityid == -1:
            ship = sandbox.createEntity()
        else:
            ship = sandbox.addEntity(entityid)
        if playerShip:
            component = shipComponents.PlayerComponent()
            ship.addComponent(component)
        else:
            component = shipComponents.AIPilotComponent()
            ship.addComponent(component)
        shape = BulletSphereShape(1)
        velocity = Vec3(0, 0, 0)
        truex = spawnPoint.getX()
        truey = spawnPoint.getY()
        component = physics.addNewBody(shipName, shape, self.shipClasses[shipClass]['mass'], truex, truey, velocity)
        ship.addComponent(component)
        component = shipComponents.ThrustComponent()
        for engine in self.shipClasses[shipClass]['engines']:
            component.forward += engine['thrust'] / CONVERT
        component.heading = self.shipClasses[shipClass]['torque'] / CONVERT
        ship.addComponent(component)
        component = shipComponents.InfoComponent()
        component.shipClass = shipClass
        component.name = shipName
        ship.addComponent(component)

        component = graphicsComponents.RenderComponent()
        #component.mesh = sandbox.base.loader.loadModel('ships/' + self.shipClasses[shipClass]['path'])
        component.mesh = Actor('ships/' + self.shipClasses[shipClass]['path'])
        component.mesh.reparentTo(sandbox.ships)
        component.mesh.getPart('modelRoot').setPythonTag('entityID', ship.id)
        component.mesh.setScale(1 / CONVERT)
        if universals.runClient and not playerShip:
            sandbox.send('makePickable', [component.mesh])
        ship.addComponent(component)

        # Load turret info here. Also check if gun is actually on ship!
        def containsAny(string, check):
            return 1 in [c in string for c in check]

        turretsComponent = shipComponents.TurretsComponent()

        if not turrets:
            print "Not turrets"
            for weapon in self.shipClasses[shipClass]['weapons']:
                turretEntity = sandbox.createEntity()
                turret = shipComponents.TurretComponent()
                if not containsAny(self.shipClasses[shipClass]['weapons'][weapon]['decay'], 'abcdefghijklmnopqrstuvwyz'):
                    turret.decay = lambda x: eval(self.shipClasses[shipClass]['weapons'][weapon]['decay'])
                turret.name = weapon
                turret.damage = self.shipClasses[shipClass]['weapons'][weapon]['damage']
                if 'traverser' in self.shipClasses[shipClass]['weapons'][weapon]['joints']:
                    turret.traverser = self.shipClasses[shipClass]['weapons'][weapon]['joints']['traverser']['axes']
                if 'elevator' in self.shipClasses[shipClass]['weapons'][weapon]['joints']:
                    turret.elevator = self.shipClasses[shipClass]['weapons'][weapon]['joints']['elevator']['axes']
                turret.parentID = ship.id
                turretEntity.addComponent(turret)
                turretsComponent.turretIDs.append(turretEntity.id)
        if turrets:
            print "Turrets"
            for t in turrets:
                turretEntity = sandbox.addEntity(t.turretid)
                turret = shipComponents.TurretComponent()
                weapon = turret.turretName
                if not containsAny(self.shipClasses[shipClass]['weapons'][weapon]['decay'], 'abcdefghijklmnopqrstuvwyz'):
                    turret.decay = lambda x: eval(self.shipClasses[shipClass]['weapons'][weapon]['decay'])
                turret.name = weapon
                turret.damage = self.shipClasses[shipClass]['weapons'][weapon]['damage']
                if 'traverser' in self.shipClasses[shipClass]['weapons'][weapon]['joints']:
                    turret.traverser = self.shipClasses[shipClass]['weapons'][weapon]['joints']['traverser']['axes']
                if 'elevator' in self.shipClasses[shipClass]['weapons'][weapon]['joints']:
                    turret.elevator = self.shipClasses[shipClass]['weapons'][weapon]['joints']['elevator']['axes']
                turret.parentID = ship.id
                turretEntity.addComponent(turret)
                turretsComponent.turretIDs.append(turretEntity.id)

        ship.addComponent(turretsComponent)

        #sandbox.send("shipGenerated", [ship, playerShip])
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
                    sandbox.send('stationEmptied', [ship.id, stationName])
