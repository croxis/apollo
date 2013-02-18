from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape, BulletWorld
from panda3d.core import NodePath, Point3, Vec3

import sandbox

import shipComponents
import solarSystem
import universals

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "notify-level-ITF-PhysicsSystem debug")
from direct.directnotify.DirectNotify import DirectNotify
log = DirectNotify().newCategory("ITF-PhysicsSystem")

# Size of the bulletworld. We keep to positive just for the sake of sanity
ZONESIZE = 1000000

'''worlds[x][y] = (BulletWorld(), NodePath())
Each world is 1 million x 1 million km'''
worlds = {}


def setZone(component, truex, truey):
    '''Sets the zone for the component if different than current based on new coords'''
    zonex, zoney, subx, suby = computeZonePos(truex, truey)
    if zonex != component.zonex or zoney is not component.zoney:
        currentX = component.zonex
        currentY = component.zoney
        velocity = component.node.getLinearVelocity()
        spin = component.node.getAngularVelocity()
        oldzone = getZone(currentX, currentY)
        oldzone[0].removeRigidBody(component.node)
        zone = getZone(zonex, zoney)
        zone[0].attachRigidBody(component.node)
        component.nodePath.reparentTo(zone[1])
        component.node.setLinearVelocity(velocity)
        component.node.setAngularVelocity(spin)
        component.nodePath.setPos(subx, suby, 0)
        component.zonex = zonex
        component.zoney = zoney
        log.debug("Moved zone: " + component.nodePath.getName() + " from " + str(currentX) + ", " + str(currentY) + " to " + str(zonex) + ", " + str(zoney))


def checkZone(component):
    '''Returns boolean if the component needs to change zones'''
    changeZone = False
    pos = component.getTruePos()
    if pos.getX() >= ZONESIZE:
        changeZone = True
    elif pos.getX() < 0:
        changeZone = True
    if pos.getY() >= ZONESIZE:
        changeZone = True
    elif pos.getY() < 0:
        changeZone = True
    return changeZone


def changeZone(component):
    '''Checks if the zone needs to be changed based on current position, then
    changes it if it should'''
    if checkZone(component):
        pos = component.getTruePos()
        setZone(component, pos.getX(), pos.getY())


def computeZonePos(truex, truey):
    '''Converts the true position into zone x, y and the local zone coords'''
    zonex = int(truex / ZONESIZE)
    if zonex < 0:
        zonex -= 1
    zoney = int(truey / ZONESIZE)
    if zoney < 0:
        zoney -= 1
    #subx = truex % ZONESIZE
    #suby = truey % ZONESIZE
    subx = truex - zonex * ZONESIZE
    suby = truey - zoney * ZONESIZE
    return zonex, zoney, subx, suby


def getZone(zonex, zoney):
    if zonex not in worlds:
        worlds[zonex] = {}
    if zoney not in worlds[zonex]:
        worlds[zonex][zoney] = (BulletWorld(), NodePath('Zone ' + str(zonex) + str(zoney)))
        worlds[zonex][zoney][0].setGravity((0, 0, 0))
        log.debug("Zone added: " + str(zonex) + ", " + str(zoney))
    return worlds[zonex][zoney]


def addNewBody(name, shape, mass, truex=0, truey=0, velocity=Vec3(0, 0, 0)):
    '''Adds a new BulletRidgedBody at position truex and truey.
    shape is a BulletShape, mass in kg

    Returns BulletPhysicsComponent'''
    zonex, zoney, subx, suby = computeZonePos(truex, truey)
    zone = getZone(zonex, zoney)
    component = shipComponents.BulletPhysicsComponent()
    component.bulletShape = shape
    component.node = BulletRigidBodyNode(name)
    component.node.setMass(mass)
    component.node.addShape(component.bulletShape)
    component.nodePath = zone[1].attachNewNode(component.node)
    component.currentSOI = universals.defaultSOIid
    component.nodePath.setPos(subx, suby, 0)
    component.node.setLinearVelocity(velocity)
    component.node.setAngularSleepThreshold(0.01)
    zone[0].attachRigidBody(component.node)
    '''component.debugNode = BulletDebugNode(shipName + "_debug")
    component.debugNode.showWireframe(True)
    component.debugNode.showConstraints(True)
    component.debugNode.showBoundingBoxes(True)
    component.debugNode.showNormals(True)
    component.debugNodePath = sandbox.base.render.attachNewNode(component.debugNode)
    component.debugNodePath.show()'''
    component.zonex = zonex
    component.zoney = zoney
    log.debug("Component added: " + name + " at " + str(truex) + ", " + str(truey))
    log.debug("Component verification: " + str(component.getTruePos()))
    return component


def getPhysics():
    return sandbox.getSystem(PhysicsSystem)


'''def getPhysicsWorld():
    return sandbox.getSystem(PhysicsSystem).world


def addBody(body):
    getPhysicsWorld().attachRigidBody(body)'''


class PhysicsSystem(sandbox.EntitySystem):
    """System that interacts with the Bullet physics world.
    Meshes are made in standard SI (meters, newtons).
    Internally we autoscale down to km. A factor of 1000.
    IE 1 blender unit = 1 m. 1 panda unit = 1 km.
    Configuration files units are km, metric ton, kilonewtons"""
    #TODO: Scale config to standard SI and programmaticly adjust to
    # km metric ton and kilonewtons
    def init(self):
        #self.accept("addSpaceship", self.addSpaceship)
        self.accept('setThrottle', self.setThrottle)
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
            distance = (bodyComponent.truePos - shipPhysics.getTruePos()).length()
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
        vector = celestial.truePos - shipPhysics.getTruePos()
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
        #force = thrust / 1000.0
        force = thrust
        shipPhysics.node.applyCentralForce(force)
        shipPhysics.node.applyTorque(Vec3(0, 0, -shipPhysics.currentTorque))
        #shipPhysics.node.applyTorque(Vec3(0, 0, -1.3e+7))
        #print "beat", shipPhysics.nodePath.getHpr(), shipPhysics.node.getAngularVelocity()
        #print "Physics", shipPhysics.nodePath.getHpr(), shipPhysics.currentTorque, shipPhysics.node.getAngularVelocity()
        #print "Physics", shipPhysics.nodePath.getPos(), shipPhysics.node.getLinier
        #self.world.setDebugNode(shipPhysics.debugNode)

    def end(self):
        dt = globalClock.getDt()
        for zonex in worlds:
            for zoney in worlds[zonex]:
                worlds[zonex][zoney][0].doPhysics(dt)
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
        # Power curve should be deminishing returns, bell curve function
        power = 1.0
        shipPhysics.currentTorque = shipThrust.heading * power * data.heading / 100.0
        #shipPhysics.currentTorque = 1.3e+7
        #shipPhysics.currentTorque = shipThrust.heading / (100.0 * 4) * data.heading
        #print "SetPhysics", shipPhysics.nodePath.getHpr(), shipPhysics.currentTorque, shipPhysics.node.getAngularVelocity()
        #print shipPhysics.nodePath.getPos(), shipPhysics.node.getLinearVelocity()
