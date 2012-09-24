'''Ship components'''


class BulletPhysicsComponent(object):
    '''Contains reference to bullet shape and node as well as SOI for
    planetary gravitational influence'''
    bulletShape = None
    node = None
    nodePath = None
    debugNode = None
    debugNodePath = None
    currentThrust = 0
    currentTorque = 0
    currentSOI = None  # EntityID


class AIPilotComponent(object):
    ai = None


class PlayerComponent(object):
    '''These are given NetAddresses'''
    navigation = 0


class ThrustComponent(object):
    '''Maximum thrust values, in newtons. Rotational in Newton Meters'''
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
