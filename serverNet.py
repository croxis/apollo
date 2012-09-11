import sys
sys.path.append('..')
import sandbox

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "notify-level-ITF-ServerNetwork debug")
from direct.directnotify.DirectNotify import DirectNotify
log = DirectNotify().newCategory("ITF-ServerNetwork")

import datetime

from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from panda3d.core import ConnectionWriter, NetDatagram, QueuedConnectionManager, QueuedConnectionReader

import protocol
import shipComponents
import universals
import shipSystem

import yaml

class AccountComponent(object):
    address = None

class NetworkSystem(sandbox.EntitySystem):
    def init(self, port=1999, backlog=1000, compress=False):
        log.debug("Initiating Network System")
        self.accept("broadcastData", self.broadcastData)
        self.port = port
        self.backlog = backlog
        self.compress = compress

        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        #self.cReader.setRawMode(True)
        self.cWriter = ConnectionWriter(self.cManager, 0)
        self.udpSocket = self.cManager.openUDPConnection(self.port)
        self.cReader.addConnection(self.udpSocket)

        self.activePlayers = []  # PlayerComponent
        self.activeConnections = {}  # {NetAddress : PlayerComponent}
        self.shipMap = {} # {ShipID: {CONSOL: Netaddress}}
        self.lastAck = {}  # {NetAddress: time}

        self.startPolling()
        #self.accept("shipGenerated", self.shipGenerated)

    def startPolling(self):
        #taskMgr.add(self.tskReaderPolling, "serverListenTask", -40)
        sandbox.base.taskMgr.doMethodLater(10, self.activeCheck, "activeCheck")

    #def tskReaderPolling(self, taskdata):
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

                self.lastAck[datagram.getAddress()] = datetime.datetime.now()
                #TODO Switch to ip address and port

                #Order of these will need to be optimized later
                #We now pull out the rest of our headers
                remotePacketCount = myIterator.getUint8()
                ack = myIterator.getUint8()
                acks = myIterator.getUint16()
                hashID = myIterator.getUint16()
                protobuf = myIterator.getUint8()

                if msgID == protocol.REQUEST_STATIONS:
                    shipname = myIterator.getString()
                    stations = yaml.load(myIterator.getString())
                    print shipname, stations
                elif msgID == protocol.LOGIN:
                    #TODO, if connection previously existed, reconnect
                    #TODO: send current mission status.
                    #ackDatagram = protocol.loginAccepted(entity.id)
                    #self.sendData(ackDatagram, datagram.getAddress())
                    shipSys = sandbox.getSystem(shipSystem.ShipSystem)
                    ackDatagram = protocol.shipClasses(shipSys.shipClasses)
                    self.sendData(ackDatagram, datagram.getAddress())
                    ackDatagram = protocol.genericPacket(protocol.PLAYER_SHIPS)
                    entities = shipSys.getPlayerShipEntities()
                    db = {}
                    for entity in entities:
                        db[entity.id] = {}
                        info = entity.getComponent(shipComponents.InfoComponent)
                        db[entity.id]['name'] = info.name
                        db[entity.id]['class'] = info.shipClass
                        player = entity.getComponent(shipComponents.PlayerComponent)
                        db[entity.id]['stations'] = {}
                        db[entity.id]['stations']['navigation'] = player.navigation
                    print "DB", db, yaml.dump(db)
                    ackDatagram.addString(yaml.dump(db))
                    self.sendData(ackDatagram, datagram.getAddress())
                    entity = sandbox.createEntity()
                    component = AccountComponent()
                    component.address = datagram.getAddress()
                    entity.addComponent(component)
                    self.activeConnections[component.address] = component
                    '''if username not in accountEntities:
                        entity = sandbox.createEntity()
                        component = AccountComponent()
                        component.name = username
                        component.passwordHash = password
                        if not accountEntities:
                            component.owner = True
                        component.address = datagram.getAddress()
                        entity.addComponent(component)
                        accountEntities[username] = entity.id
                        log.info("New player " + username + " logged in.")
                        #
                        self.activePlayers.append(component)
                        self.activeConnections[component.address] = component
                        ackDatagram = protocol.loginAccepted(entity.id)
                        self.sendData(ackDatagram, datagram.getAddress())
                        #TODO: Send initial states?
                        #messenger.send("newPlayerShip", [component, entity])
                    else:
                        component = sandbox.entities[accountEntities[username]].getComponent(AccountComponent)
                        if component.passwordHash != password:
                            log.info("Player " + username + " has the wrong password.")
                        else:
                            component.connection = datagram.getConnection()
                            log.info("Player " + username + " logged in.")'''

    def activeCheck(self, task):
        """Checks for last ack from all known active connections."""
        for address, lastTime in self.lastAck.items():
            if (datetime.datetime.now() - lastTime).seconds > 30:
                print self.activeConnections
                component = self.activeConnections[address]
                #TODO: Disconnect
        return task.again

    def sendData(self, datagram, address):
        self.cWriter.send(datagram, self.udpSocket, address)

    def broadcastData(self, datagram):
        # Broadcast data out to all activeConnections
        #for accountID in accountEntities.items():
            #sandbox.entities[accountID].getComponent()
        for addr in self.activeConnections.keys():
            self.sendData(datagram, addr)

    def processData(self, netDatagram):
        myIterator = PyDatagramIterator(netDatagram)
        return self.decode(myIterator.getString())

    def shipGenerated(self, ship):
        datagram = protocol.newShip(ship)
        print "Checking if new ship is valid for udp:", self.cWriter.isValidForUdp(datagram)
        self.broadcastData(datagram)

class ClientComponent:
    """Theoretical component that stores which clients are 
    also tracking this entity as well as last update"""