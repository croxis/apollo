from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape, BulletWorld
from panda3d.core import Point3, Vec3

import sandbox

import shipComponents
import solarSystem
import universals


def getPhysics():
    return sandbox.getSystem(PhysicsSystem)


def getPhysicsWorld():
    return sandbox.getSystem(PhysicsSystem).world


def addBody(body):
    getPhysicsWorld().attachRigidBody(body)


class PhysicsSystem(sandbox.EntitySystem):
    """System that interacts with the Bullet physics world"""
    def init(self):
        #self.accept("addSpaceship", self.addSpaceship)
        self.accept('setThrottle', self.setThrottle)
        self.world = BulletWorld()

    def begin(self):
        dt = sandbox.base.globalClock.getDt()
        self.world.doPhysics(dt)
        #world.doPhysics(dt, 10, 1.0/180.0)

    def process(self, entity):
        shipPhysics = entity.getComponent(shipComponents.BulletPhysicsComponent)
        shipPhysics.node.applyCentralForce((0, shipPhysics.currentThrust, 0))

    def setThrottle(self, shipid, data):
        if abs(data.normal) > 100:
            return
        ship = sandbox.entities[shipid]
        shipPhysics = ship.getComponent(shipComponents.BulletPhysicsComponent)
        shipThrust = ship.getComponent(shipComponents.ThrustComponent)
        shipPhysics.currentThrust = shipThrust.forward * data.normal
        #ship.getComponent(shipComponents.BulletPhysicsComponent).node.applyCentralForce((0, force, 0))

    '''def addSpaceship(self, component, accountName, position, linearVelcocity):
        component.bulletShape = BulletSphereShape(5)
        component.node = BulletRigidBodyNode(accountName)
        component.node.setMass(1.0)
        component.node.addShape(component.bulletShape)
        component.nodePath = universals.solarSystemRoot.attachNewNode(component.node)
        addBody(component.node)
        position = sandbox.getSystem(solarSystem.SolarSystemSystem).solarSystemRoot.find("**/Earth").getPos()
        #component.nodePath.setPos(position + Point3(6671, 0, 0))
        component.nodePath.setPos(position)
        #component.node.setLinearVelocity(Vec3(0, 7.72983, 0))
        component.node.setLinearVelocity(linearVelcocity)'''
