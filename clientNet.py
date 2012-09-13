import sandbox
from panda3d.core import Point3, VBase3, Vec3
from panda3d.core import QueuedConnectionManager, QueuedConnectionReader, ConnectionWriter, NetAddress, NetDatagram
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

import protocol
import shipComponents
import universals
from universals import log

import yaml

#PROPOSAL! {server entity id: client entity id} and reverse lookup dict too

class NetworkSystem(sandbox.UDPNetworkSystem):
    def init2(self):
        self.packetCount = 0
        self.accept('login', self.sendLogin)
        self.accept('requestStations', self.requestStations)

    def processPacket(self, msgID, remotePacketCount, ack, acks, hashID, serialized, address):
        #If not in our protocol range then we just reject
        if msgID < 0 or msgID > 200:
            return
        print msgID
        data = protocol.readProto(msgID, serialized)
        if msgID == protocol.PLAYER_SHIPS:
            sandbox.send('shipSelectScreen', [data])
        elif msgID == protocol.SHIP_CLASSES:
            sandbox.send('shipClassList', [data])
        return

        if msgID == protocol.NEW_SHIP:
            log.info("New ship")
            shipID = myIterator.getUint8()
            shipName = myIterator.getString()
            health = myIterator.getUint8()
            position = Point3(myIterator.getFloat32(), myIterator.getFloat32(), myIterator.getFloat32())
            linearVelocity = Vec3(myIterator.getFloat32(), myIterator.getFloat32(), myIterator.getFloat32())
            rotiation = VBase3(myIterator.getFloat32(), myIterator.getFloat32(), myIterator.getFloat32())
            angularVelocity = Vec3(myIterator.getFloat32(), myIterator.getFloat32(), myIterator.getFloat32())
            ship = sandbox.addEntity(shipID)
            component = ships.PilotComponent()
            component.accountEntityID = playerPilotID
            ship.addComponent(component)
            component = ships.BulletPhysicsComponent
            messenger.send("addSpaceShip", [component, shipName, position, linearVelocity])
            ship.addComponent(component)
            component = ships.ThrustComponent()
            ship.addComponent(component)
            component = ships.InfoComponent()
            component.health = health
            component.name = shipName
            ship.addComponent(component)
        elif msgID == protocol.LOGIN_ACCEPTED:
            log.info("Login accepted")
            entityID = myIterator.getUint8()
            universals.day = myIterator.getFloat32()
            print "Day set to", universals.day
        elif msgID == protocol.LOGIN_DENIED:
            log.info("Login failed")

    def sendLogin(self, serverAddress):
        self.serverAddress = serverAddress
        datagram = self.generateGenericPacket(protocol.LOGIN)
        universals.log.debug("sending login")
        self.send(datagram)


    def requestStations(self, shipid, stations):
        datagram = protocol.requestStations(shipid, stations)
        self.send(datagram)

    def send(self, datagram):
        self.sendData(datagram, self.serverAddress)


            

class ServerComponent:
    """Theoretical component for server generated and sent entities"""
    serverEntityID = 0
    lastServerUpdate = 0