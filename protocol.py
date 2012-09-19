import proto_pb2 as proto
import shipComponents
import shipSystem
import universals

import sandbox

# The proto file shouldn't be accessed directly, it should be handled in
# This file

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
#THRUST_REQ = 2
POS_PHYS_UPDATE = 3   # Full physics update for a given ship.
# 1 per second unless a non predictive force (ie non gravity) is applied
DATE_UPDATE = 5  # 1 per 5 seconds
CHAT = 6

NEW_SHIP = 9  # A ship has entered sensor range. All data is sent in this packet
NEW_STATION = 11  # A station has entered sensor range.

SET_THROTTLE = 12

LOGIN = 100
LOGIN_DENIED = 101
LOGIN_ACCEPTED = 103

SHIP_CLASSES = 105
PLAYER_SHIPS = 107

REQUEST_STATIONS = 108
CONFIRM_STATIONS = 109


# protobuf parsers
def readProto(msgID, message):
    if msgID == CONFIRM_STATIONS:
        data = proto.Ship()
    elif msgID == LOGIN:
        return
    elif msgID == PLAYER_SHIPS or msgID == REQUEST_STATIONS or msgID == POS_PHYS_UPDATE:
        data = proto.Ships()
    elif msgID == SET_THROTTLE:
        data = proto.Throttle()
    elif msgID == SHIP_CLASSES:
        data = proto.ShipClasses()
    else:
        return
    data.ParseFromString(message)
    return data


#Client to server datagram generators
def requestStations(shipid, stations):
    playerShips = proto.Ships()
    playerShip = playerShips.ship.add()
    playerShip.id = shipid
    #shipStations = playerShip.stations.add()
    shipStations = playerShip.stations
    for station in stations:
        setattr(shipStations, station, 1)
    return sandbox.generatePacket(REQUEST_STATIONS, playerShips)


def requestThrottle(throttle):
    t = proto.Throttle()
    t.normal = throttle
    return sandbox.generatePacket(SET_THROTTLE, t)


#Server to client datagram generators


'''def loginAccepted(x):
    datagram = genericPacket(LOGIN_ACCEPTED)
    datagram.addUint8(x)  # entity id of user
    datagram.addFloat32(universals.day)
    return datagram'''


def confirmStations(shipid, stations):
    ship = proto.Ship()
    ship.id = shipid
    shipEntity = sandbox.entities[shipid]
    info = shipEntity.getComponent(shipComponents.InfoComponent)
    ship.name = info.name
    ship.className = info.shipClass
    shipPhysics = shipEntity.getComponent(shipComponents.BulletPhysicsComponent)
    packFullPhysics(shipPhysics, ship)
    #shipStations = ship.stations.add()
    shipStations = ship.stations
    for station in stations:
        setattr(shipStations, station, 1)
    datagram = sandbox.generatePacket(CONFIRM_STATIONS, ship)
    return datagram


def shipClasses(db):
    shipClasses = proto.ShipClasses()
    for shipClass in db:
        ship = shipClasses.shipClass.add()
        ship.className = db[shipClass]['class']
        ship.mass = int(db[shipClass]['mass'])
        ship.meshName = db[shipClass]['mesh']
        ship.folderName = db[shipClass]['folder']
    datagram = sandbox.generatePacket(SHIP_CLASSES, shipClasses)
    return datagram


def packFullPhysics(shipPhysics, ship):
    ship.x = shipPhysics.nodePath.getX()
    ship.y = shipPhysics.nodePath.getY()
    ship.h = shipPhysics.nodePath.getH()
    ship.dx = shipPhysics.node.getLinearVelocity()[0]
    ship.dy = shipPhysics.node.getLinearVelocity()[1]
    ship.dh = shipPhysics.node.getAngularVelocity()[0]
    ship.thrust = shipPhysics.currentThrust


def playerShipStations():
    shipSys = sandbox.getSystem(shipSystem.ShipSystem)
    playerShips = proto.Ships()
    entities = shipSys.getPlayerShipEntities()
    for entity in entities:
        playerShip = playerShips.ship.add()
        info = entity.getComponent(shipComponents.InfoComponent)
        shipPhysics = entity.getComponent(shipComponents.BulletPhysicsComponent)
        playerShip.name = info.name
        playerShip.className = info.shipClass
        playerShip.id = entity.id
        packFullPhysics(shipPhysics, playerShip)
        player = entity.getComponent(shipComponents.PlayerComponent)
        shipStations = playerShip.stations
        stations = vars(player)
        for stationName, status in stations.items():
            if status == 0:
                setattr(shipStations, stationName, 0)
            else:
                setattr(shipStations, stationName, 1)
    return sandbox.generatePacket(PLAYER_SHIPS, playerShips)


def sendShipUpdates(shipEntities):
    ships = proto.Ships()
    for shipEntity in shipEntities:
        ship = ships.ship.add()
        ship.id = shipEntity.id
        component = shipEntity.getComponent(shipComponents.BulletPhysicsComponent)
        packFullPhysics(component, ship)
        ship.name = shipEntity.getComponent(shipComponents.InfoComponent).name
        ship.className = shipEntity.getComponent(shipComponents.InfoComponent).shipClass
    return sandbox.generatePacket(POS_PHYS_UPDATE, ships)
