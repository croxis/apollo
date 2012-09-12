import sys
sys.path.append('..')
import sandbox

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "notify-level-ITF-ServerNetwork debug")
from direct.directnotify.DirectNotify import DirectNotify
log = DirectNotify().newCategory("ITF-ServerNetwork")

import datetime
import socket

import protocol
import shipComponents
import universals
import shipSystem

import yaml

from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from panda3d.core import ConnectionWriter, NetDatagram, QueuedConnectionManager, QueuedConnectionReader

class AccountComponent(object):
    address = None

class NetworkSystem(sandbox.UDPNetworkSystem):
    def init2(self):
        self.accept("broadcastData", self.broadcastData)
        self.accept("confirmPlayerStations", self.confirmPlayerStations)

        self.activePlayers = []  # PlayerComponent
        self.activeConnections = {}  # {NetAddress : PlayerComponent}
        #self.shipMap = {} # {ShipID: {CONSOL: Netaddress}}
        #self.accept("shipGenerated", self.shipGenerated)


    #def tskReaderPolling(self, taskdata):
    def processPacket(self, msgID, remotePacketCount, ack, acks, hashID, serialized):
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
            #print "Data", datagram.getConnection(), datagram.getAddress(), datagram.getAddress().getPort()
            if msgID == protocol.REQUEST_STATIONS:
                print self.activeConnections
                #if self.n == datagram.getAddress():
                #    print "yay"
                #else:
                #    print "===nay==="
                #    print datagram.getAddress(), datagram.getAddress().getPort()
                #    print self.n, self.n.getPort()
                shipname = myIterator.getString()
                stations = yaml.load(myIterator.getString())
                shipSys = sandbox.getSystem(shipSystem.ShipSystem)
                entities = shipSys.getPlayerShipEntities()
                db = {}
                for entity in entities:
                    info = entity.getComponent(shipComponents.InfoComponent)
                    if shipname == info.name:
                        player = entity.getComponent(shipComponents.PlayerComponent)
                        for station in stations:
                            if getattr(player, station) != 0:
                                print "Resend ship select window"
                        sandbox.send('setPlayerStations', [datagram.getAddress(), shipname, stations])
            elif msgID == protocol.LOGIN:
                #TODO, if connection previously existed, reconnect
                #TODO: send current mission status.
                #ackDatagram = protocol.loginAccepted(entity.id)
                #self.sendData(ackDatagram, datagram.getAddress())
                #TODO: Move ship select to separate function
                #self.n = datagram.getAddress()
                #print "======"
                #print datagram.getAddress(), datagram.getAddress().getPort(), self.n, self.n.getPort()
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
                print self.activeConnections
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

    def broadcastData(self, datagram):
        # Broadcast data out to all activeConnections
        #for accountID in accountEntities.items():
            #sandbox.entities[accountID].getComponent()
        for addr in self.activeConnections.keys():
            self.sendData(datagram, addr)

    def confirmPlayerStations(self, netAddress, stations):
        datagram = protocol.confirmStations(stations)
        self.sendData(datagram, netAddress)

class ClientComponent:
    """Theoretical component that stores which clients are 
    also tracking this entity as well as last update"""
