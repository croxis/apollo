import shipComponents
import universals

#Client to server even
#Server to client odd
#If both will probably be even

# Packet structure
# msgID = myIterator.getUint8()
# remotePacketCount = myIterator.getUint8()
# ack = myIterator.getUint8()
# acks = myIterator.getUint16()
# hashID = myIterator.getUint16()
# protobuf
# When compiled: "msgID, remotePacketCount, ack, acks, hashID, protobuf"

#Protocol space
#0-99 common game elements
#100-199 login and server handshaking and admin stuff

ACK = 0
POS_UPDATE = 1  # Position update for a given ship.  1 - 10 times a second
THRUST_REQ = 2
POS_PHYS_UPDATE = 3   # Full physics update for a given ship.
# 1 per second unless a non predictive force (ie non gravity) is applied
DATE_UPDATE = 5  # 1 per 5 seconds
CHAT = 6

NEW_SHIP = 9  # A ship has entered sensor range. All data is sent in this packet
NEW_STATION = 11  # A station has entered sensor range.

LOGIN = 100
LOGIN_DENIED = 101
LOGIN_ACCEPTED = 103

SHIP_CLASSES = 105
PLAYER_SHIPS = 107

REQUEST_STATIONS = 108
CONFIRM_STATIONS = 109

def unpackPacket(datagram):
    split = datagram.split(',',5)
    return int(split[0]), int(split[1]), int(split[2]), int(split[3]), int(split[4]), split[5]

def genericPacket(key, packetCount=0):
    datagram = str(key) + ',' + '0,0,0,0'
    return datagram

#Client to server datagram generators

def requestStations(name, stations):
    datagram = genericPacket(REQUEST_STATIONS)
    datagram.addString(name)
    datagram.addString(yaml.dump(stations))
    return datagram


#Server to client datagram generators


def loginAccepted(x):
    datagram = genericPacket(LOGIN_ACCEPTED)
    datagram.addUint8(x)  # entity id of user
    datagram.addFloat32(universals.day)
    return datagram

def confirmStations(stations):
    datagram = genericPacket(CONFIRM_STATIONS)
    datagram.addString(yaml.dump(stations))
    return datagram


# Depreciate. Move to a universal ship entering sensorrange, even if
# Ship spawns inside sensors
def newShip(ship):
    datagram = genericPacket(NEW_SHIP)
    datagram.addUint8(ship.id)
    datagram.addString(ship.getComponent(ships.InfoComponent).name)
    datagram.addUint8(ship.getComponent(ships.InfoComponent).health)
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).nodePath.getX())
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).nodePath.getY())
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).nodePath.getZ())
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).node.getLinearVelocity().x)
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).node.getLinearVelocity().y)
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).node.getLinearVelocity().z)
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).nodePath.getH())
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).nodePath.getP())
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).nodePath.getR())
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).node.getAngularVelocity().x)
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).node.getAngularVelocity().y)
    datagram.addFloat32(ship.getComponent(ships.BulletPhysicsComponent).node.getAngularVelocity().z)
    return datagram


def shipClasses(db):
    datagram = genericPacket(SHIP_CLASSES)
    datagram.addString(yaml.dump(db))
    return datagram
