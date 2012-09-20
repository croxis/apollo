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
        self.world.setGravity((0, 0, 0))
        self.counter = 0

    def process(self, entity):
        shipPhysics = entity.getComponent(shipComponents.BulletPhysicsComponent)
        if not shipPhysics.node.is_active():
            shipPhysics.node.setActive(True)
        shipPhysics.node.applyCentralForce(Vec3(0, shipPhysics.currentThrust, 0))
        shipPhysics.node.applyTorque(Vec3(0, 0, -shipPhysics.currentTorque))
        self.world.setDebugNode(shipPhysics.debugNode)

    def end(self):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)
        #self.world.doPhysics(dt, 10, 1.0 / 180.0)

    def setThrottle(self, shipid, data):
        if abs(data.normal) > 100 or abs(data.heading) > 100:
            print "Invalid"
            return
        ship = sandbox.entities[shipid]
        shipPhysics = ship.getComponent(shipComponents.BulletPhysicsComponent)
        shipThrust = ship.getComponent(shipComponents.ThrustComponent)
        shipPhysics.currentThrust = shipThrust.forward / 100.0 * data.normal
        shipPhysics.currentTorque = shipThrust.heading / 100.0 * data.heading

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
