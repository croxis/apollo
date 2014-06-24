__author__ = 'croxis'

import sandbox
import capnp

capnp.remove_import_hook()
proto = capnp.load('protocol.capnp')


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

SET_TARGET = 14

LOGIN = 100
LOGIN_DENIED = 101
LOGIN_ACCEPTED = 103

SHIP_CLASSES = 105
PLAYER_SHIPS = 107

REQUEST_STATIONS = 108
CONFIRM_STATIONS = 109
REQUEST_CREATE_SHIP = 110


#Client to server datagram generators
def request_stations(shipid, stations):
    playerShips = proto.Ships.new_message()
    playerShip = playerShips.ship.add()
    playerShip.id = shipid
    shipStations = playerShip.stations
    for station in stations:
        setattr(shipStations, station, 1)
    return sandbox.generatePacket(REQUEST_STATIONS, playerShips)


def request_throttle(throttle, heading):
    t = proto.Throttle.new_message()
    t.normal = throttle
    t.heading = heading
    return sandbox.generatePacket(SET_THROTTLE, t)


def request_create_ship(name, className):
    ship = proto.Ship.new_message()
    ship.id = -1
    ship.name = name
    ship.className = className
    return sandbox.generatePacket(REQUEST_CREATE_SHIP, ship)


def request_turret_target(targetId, turretId=None):
    turret = proto.Target.new_message()
    turret.targetId = targetId
    if turretId:
        turret.turretId = turretName
    return sandbox.generatePacket(SET_TARGET, turret)


#Server to client datagram generators


'''def loginAccepted(x):
    datagram = genericPacket(LOGIN_ACCEPTED)
    datagram.addUint8(x)  # entity id of user
    datagram.addFloat32(universals.day)
    return datagram'''


def confirmStations(shipid, stations):
    ship = proto.Ship.new_message()
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
    shipClasses = proto.ShipClasses.new_message()
    for shipClass in db:
        ship = shipClasses.shipClass.add()
        ship.className = db[shipClass]['class']
        ship.mass = int(db[shipClass]['mass'])
        ship.meshName = db[shipClass]['mesh']
        ship.folderName = db[shipClass]['folder']
    datagram = sandbox.generatePacket(SHIP_CLASSES, shipClasses)
    return datagram


def packFullPhysics(shipPhysics, ship):
    ship.x = shipPhysics.getTruePos().getX()
    ship.y = shipPhysics.getTruePos().getY()
    ship.h = shipPhysics.nodePath.getH()
    ship.dx = shipPhysics.node.getLinearVelocity()[0]
    ship.dy = shipPhysics.node.getLinearVelocity()[1]
    ship.dh = shipPhysics.node.getAngularVelocity()[2]
    ship.thrust = shipPhysics.currentThrust
    ship.torque = shipPhysics.currentTorque


def playerShipStations():
    shipSys = sandbox.getSystem(shipSystem.ShipSystem)
    playerShips = proto.Ships.new_message()
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
    ships = proto.Ships.new_message()
    for shipEntity in shipEntities:
        ship = ships.ship.add()
        ship.id = shipEntity.id
        component = shipEntity.getComponent(shipComponents.BulletPhysicsComponent)
        packFullPhysics(component, ship)
        ship.name = shipEntity.getComponent(shipComponents.InfoComponent).name
        ship.className = shipEntity.getComponent(shipComponents.InfoComponent).shipClass
        turrets = shipEntity.getComponent(shipComponents.TurretsComponent)
        mesh = shipEntity.getComponent(graphicsComponents.RenderComponent).mesh
        for turretEntityID in turrets.turretIDs:
            turret = ship.turrets.add()
            turret.turretid = turretEntityID

            turretComponent = sandbox.entities[turretEntityID].getComponent(shipComponents.TurretComponent)
            turret.turretName = turretComponent.name

            joint = turret.joints.add()
            # Using "targetHPR" as current HPR for now
            fullJoint = 'gun-' + turretComponent.name.replace(' ', '_') + "-elevator"
            joint.jointName = "elevator"
            joint.time = 0
            joint.targetH = mesh.controlJoint(None, "modelRoot", fullJoint).getH()
            joint.targetP = mesh.controlJoint(None, "modelRoot", fullJoint).getP()
            joint.targetR = mesh.controlJoint(None, "modelRoot", fullJoint).getR()

            joint = turret.joints.add()
            # Using "targetHPR" as current HPR for now
            fullJoint = joint.jointName = 'gun-' + turretComponent.name.replace(' ', '_') + "-traverser"
            joint.jointName = "traverser"
            joint.time = 0
            joint.targetH = mesh.controlJoint(None, "modelRoot", fullJoint).getH()
            joint.targetP = mesh.controlJoint(None, "modelRoot", fullJoint).getP()
            joint.targetR = mesh.controlJoint(None, "modelRoot", fullJoint).getR()

    return sandbox.generatePacket(POS_PHYS_UPDATE, ships)