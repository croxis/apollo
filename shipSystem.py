import sandbox

from direct.stdpy.file import *

from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape
from panda3d.core import Point3, Vec3

import physics
import shipComponents
import solarSystem
import universals

import glob
import yaml



class ShipSystem(sandbox.EntitySystem):
    def init(self):
        #self.accept("newPlayerShip", self.newPlayerShip)
        self.shipClasses = {}

    def process(self, entity):
        pass

    def loadShipClasses(self):
        shippaths = glob.glob('ships/*/ship.yaml')
        for yamlPath in shippaths:
            shipFile = open(yamlPath)
            ship = yaml.load(shipFile)
            ship['path'] = 'ships/' + ship['mesh'] + '/'
            shipFile.close()
            #TODO switch class name to folder name
            self.shipClasses[ship['mesh']] = ship
            universals.log.info("Loaded " + ship['mesh'])

    def newShip(self, shipName, shipClass, playerShip=False):
        ship = sandbox.createEntity()
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
        sandbox.send("shipGenerated", [ship])
        universals.log.info("Ship spawned: " + shipName + " " + shipClass)
        #messenger.send("putPlayerOnShip", [accountEntity.id, ship.id])
        #TODO Transmit player's ship data
        #TODO Broadcast new ship data
        #TODO Prioritize updating new client of surroundings

    def getPlayerShipEntities(self):
        return sandbox.getEntitiesByComponentType(shipComponents.PlayerComponent)
