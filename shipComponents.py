'''Ship components'''
from panda3d.core import LPoint3d

import physics

'''The following represent the more "physical" components that represent a ship'''


class BulletPhysicsComponent(object):
    '''Contains reference to bullet shape and node as well as SOI for
    planetary gravitational influence.

    zonex and zoney is the id of the bullet world. The true
    position is is worldx + nodePath.getX()'''
    bulletShape = None
    node = None
    nodePath = None
    debugNode = None
    debugNodePath = None
    currentThrust = 0
    currentTorque = 0
    currentSOI = None  # EntityID
    zonex = 0
    zoney = 0

    def getTruePos(self, debug=False):
        '''Returns the "true" position of this object'''
        if debug:
            print self.nodePath.getName(), self.zoney * physics.ZONESIZE, self.nodePath.getY(), self.zoney * physics.ZONESIZE + self.nodePath.getY()
        return LPoint3d(
            self.zonex * physics.ZONESIZE + self.nodePath.getX(),
            self.zoney * physics.ZONESIZE + self.nodePath.getY(),
            self.nodePath.getZ()
        )

    def setTruePos(self, truex, truey):
        '''Converts the true pos into the proper zone system'''
        physics.setZone(self, truex, truey)


class AIPilotComponent(object):
    ai = None


class PlayerComponent(object):
    '''These are given NetAddresses'''
    navigation = 0
    mainScreen = 0
    weapons = 0


class ThrustComponent(object):
    '''Maximum thrust values, in kilonewtons. Rotational in kiloNewton kiloMeters'''
    forward = 1
    backwards = 1
    lateral = 1
    heading = 1
    yaw = 1
    roll = 1


class InfoComponent(object):
    health = 100
    name = "A ship"
    shipClass = ""


class TurretsComponent(object):
    '''Tracks the child turret entities'''
    turretIDs = []


class TurretComponent(object):
    parentID = None  # In good practice the parent pointer should be its
    # own component. We will move to this if a gun entity uses more than
    # this component
    name = ''
    damage = 0
    speed = 0 # Speed of weapon in km/s
    decay = lambda x: x
    traverser = {}  # {'y': -1}
    elevator = {}  # {'x': [-90, 0]}
    targetID = None


'''The following components represent the stations found on a ship.
These values are manipulated by the player or AI'''
