import sandbox
from panda3d.core import Point3, VBase3, Vec3
from panda3d.core import QueuedConnectionManager, QueuedConnectionReader, ConnectionWriter, NetAddress, NetDatagram
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

import protocol
import shipComponents
import universals
from universals import log

#PROPOSAL! {server entity id: client entity id} and reverse lookup dict too


class NetworkSystem(sandbox.UDPNetworkSystem):
    def init2(self):
        self.packetCount = 0
        self.accept('login', self.sendLogin)
        self.accept('requestStations', self.requestStations)
        self.accept('requestThrottle', self.requestThrottle)

    def processPacket(self, msgID, remotePacketCount, ack, acks, hashID, serialized, address):
        #If not in our protocol range then we just reject
        if msgID < 0 or msgID > 200:
            return
        data = protocol.readProto(msgID, serialized)
        if msgID == protocol.CONFIRM_STATIONS:
            sandbox.send('shipUpdate', [data, True])
            sandbox.send('setShipID', [data])
            sandbox.send('navigationScreen')
        elif msgID == protocol.PLAYER_SHIPS:
            sandbox.send('shipSelectScreen', [data])
        elif msgID == protocol.POS_PHYS_UPDATE:
            sandbox.send('shipUpdates', [data])
        elif msgID == protocol.SHIP_CLASSES:
            sandbox.send('shipClassList', [data])

    def sendLogin(self, serverAddress):
        self.serverAddress = serverAddress
        datagram = self.generateGenericPacket(protocol.LOGIN)
        universals.log.debug("sending login")
        self.send(datagram)

    def requestStations(self, shipid, stations):
        datagram = protocol.requestStations(shipid, stations)
        self.send(datagram)

    def requestThrottle(self, throttle):
        datagram = protocol.requestThrottle(throttle)
        self.send(datagram)

    def send(self, datagram):
        self.sendData(datagram, self.serverAddress)


class ServerComponent:
    """Theoretical component for server generated and sent entities"""
    serverEntityID = 0
    lastServerUpdate = 0
