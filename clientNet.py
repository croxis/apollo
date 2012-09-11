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

class NetworkSystem(sandbox.EntitySystem):
    def requestStations(self, shipname, stations):
        datagram = protocol.requestStations(shipname, stations)
        self.sendData(datagram)

    def init(self, port=2000, server="127.0.0.1", serverPort=1999, backlog=1000, compress=False):
        self.packetCount = 0
        self.port = port
        self.serverPort = serverPort
        self.serverIP = server
        self.serverAddress = NetAddress()
        self.serverAddress.setHost(server, serverPort)
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

        #self.udpSocket = self.cManager.openUDPConnection(self.port)
        self.udpSocket = self.cManager.openUDPConnection()
        self.cReader.addConnection(self.udpSocket)

        self.accept('requestStations', self.requestStations)

    def begin(self):
        if self.cReader.dataAvailable():
            datagram = NetDatagram()  # catch the incoming data in this instance
            # Check the return value; if we were threaded, someone else could have
            # snagged this data before we did
            if self.cReader.getData(datagram):
                myIterator = PyDatagramIterator(datagram)
                msgID = myIterator.getUint8()

                #If not in our protocol range then we just reject
                if msgID < 0 or msgID > 200:
                    return

                #Order of these will need to be optimized later
                #We now pull out the rest of our headers
                remotePacketCount = myIterator.getUint8()
                ack = myIterator.getUint8()
                acks = myIterator.getUint16()
                hashID = myIterator.getUint16()
                protobuf = myIterator.getUint8()
                sourceOfMessage = datagram.getConnection()

                if msgID == protocol.PLAYER_SHIPS:
                    db = yaml.load(myIterator.getString())
                    sandbox.send('shipSelectScreen', [db])
                elif msgID == protocol.CONFIRM_STATIONS:
                    stations = yaml.load(myIterator.getString())
                    print "Stations", stations
                elif msgID == protocol.NEW_SHIP:
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

    def genBasicData(self, proto):
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(proto)
        myPyDatagram.addUint8(self.packetCount)
        myPyDatagram.addUint8(0)
        myPyDatagram.addUint16(0)
        myPyDatagram.addUint16(0)
        self.packetCount += 1
        return myPyDatagram

    def sendLogin(self, username, hashpassword):
        datagram = self.genBasicData(protocol.LOGIN)
        datagram.addString(username)
        datagram.addString(hashpassword)
        universals.log.debug("sending login")
        self.sendData(datagram)

    def sendData(self, datagram):
        sent = self.cWriter.send(datagram, self.udpSocket, self.serverAddress)
        while not sent:
            print "resending"
            sent = self.cWriter.send(datagram, self.udpSocket, self.serverAddress)


            

class ServerComponent:
    """Theoretical component for server generated and sent entities"""
    serverEntityID = 0
    lastServerUpdate = 0