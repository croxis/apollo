import sandbox

from direct.directnotify.DirectNotify import DirectNotify
log = DirectNotify().newCategory("Apolloe-ClientNet")

import protocol_old
import shipComponents

#PROPOSAL! {server entity id: client entity id} and reverse lookup dict too


class NetworkSystem(sandbox.UDPNetworkSystem):
    def init2(self):
        self.packet_count = 0
        self.accept('login', self.sendLogin)
        self.accept('requestStations', self.requestStations)
        self.accept('requestThrottle', self.requestThrottle)
        self.accept('requestCreateShip', self.requestCreateShip)
        self.accept('requestTarget', self.requestTarget)

    def processPacket(self, msgID, remotePacketCount, ack, acks, hashID, serialized, address):
        #If not in our protocol range then we just reject
        if msgID < 0 or msgID > 200:
            return
        data = protocol_old.readProto(msgID, serialized)
        if msgID == protocol_old.CONFIRM_STATIONS:
            sandbox.send('shipUpdate', [data, True])
            sandbox.send('setShipID', [data])
            sandbox.send('makeStationUI', [data])
        elif msgID == protocol_old.PLAYER_SHIPS:
            sandbox.send('shipUpdates', [data])
            sandbox.send('shipSelectScreen', [data])
        elif msgID == protocol_old.POS_PHYS_UPDATE:
            sandbox.send('shipUpdates', [data])
        elif msgID == protocol_old.SHIP_CLASSES:
            sandbox.send('shipClassList', [data])

    def sendLogin(self, serverAddress):
        self.serverAddress = serverAddress
        datagram = self.generateGenericPacket(protocol_old.LOGIN)
        universals.log.debug("sending login")
        self.send(datagram)

    def requestCreateShip(self, shipName, className):
        datagram = protocol_old.requestCreateShip(shipName, className)
        self.send(datagram)

    def requestStations(self, shipid, stations):
        datagram = protocol_old.requestStations(shipid, stations)
        self.send(datagram)

    def requestThrottle(self, throttle, heading):
        datagram = protocol_old.requestThrottle(throttle, heading)
        self.send(datagram)

    def requestTarget(self, targetID):
        datagram = protocol_old.requestTurretTarget(targetID)
        self.send(datagram)

    def send(self, datagram):
        self.sendData(datagram, self.serverAddress)


class ServerComponent:
    """Theoretical component for server generated and sent entities"""
    serverEntityID = 0
    lastServerUpdate = 0
