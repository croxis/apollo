from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape, BulletWorld
from panda3d.core import Vec3

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
    """System that interacts with the Bullet physics world.
    Configuration files and meshes are made in standard SI (meters, newtons).
    Internally we autoscale down to km. A factor of 1000.
    IE 1 blender unit = 1 m. 1 panda unit = 1 km"""
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
        bodies = sandbox.getEntitiesByComponentType(solarSystem.CelestialComponent)
        # Probably very expensive. Will need optimization later
        # We assume a single star solar system. Will need to update the
        # solary system structure for multiple star solar systems
        soi = False
        previousR = 0
        for body in bodies:
            bodyComponent = body.getComponent(solarSystem.CelestialComponent)
            distance = (bodyComponent.nodePath.getPos() - shipPhysics.nodePath.getPos()).length()
            if distance < bodyComponent.soi:
                if not soi:
                    previousR = distance
                    soi = True
                    shipPhysics.currentSOI = body.id
                elif distance < previousR:
                    shipPhysics.currentSOI = body.id
        if not soi:
            shipPhysics.currentSOI = universals.defaultSOIid

        body = sandbox.entities[shipPhysics.currentSOI]
        celestial = body.getComponent(solarSystem.CelestialComponent)
        vector = celestial.nodePath.getPos() - shipPhysics.nodePath.getPos()
        distance = vector.length() * 1000
        gravityForce = Vec3(0, 0, 0)
        if distance:
            gravity = universals.G * celestial.mass * shipPhysics.node.getMass() / distance ** 2
            #print "Gravity", universals.G, celestial.mass, shipPhysics.node.getMass(), distance, gravity
            gravityForce = vector * -gravity

        thrust = universals.solarSystemRoot.getRelativeVector(shipPhysics.nodePath,
            (0, shipPhysics.currentThrust, 0))

        #force = (gravityForce + thrust) / 1000.0
        #print gravityForce, thrust / 1000.0
        force = thrust / 1000.0
        shipPhysics.node.applyCentralForce(force)
        shipPhysics.node.applyTorque(Vec3(0, 0, -shipPhysics.currentTorque))
        #print "beat", shipPhysics.nodePath.getHpr(), shipPhysics.node.getAngularVelocity()
        #print "Physics", shipPhysics.nodePath.getHpr(), shipPhysics.currentTorque, shipPhysics.node.getAngularVelocity()
        #self.world.setDebugNode(shipPhysics.debugNode)

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
        shipPhysics.currentThrust = shipThrust.forward / (100.0 * 4) * data.normal
        # Divide thrust by 400 as max thrust should be when engineering overloads
        # Power to engines. Current max overload is 400%
        # TODO: Revisit caulculation when enginerring power is added
        shipPhysics.currentTorque = shipThrust.heading / (100.0 * 4) * data.heading
        print "SetPhysics", shipPhysics.nodePath.getHpr(), shipPhysics.currentTorque, shipPhysics.node.getAngularVelocity()
