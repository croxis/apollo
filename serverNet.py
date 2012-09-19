import sys
sys.path.append('..')
import sandbox

from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "notify-level-ITF-ServerNetwork debug")
from direct.directnotify.DirectNotify import DirectNotify
log = DirectNotify().newCategory("ITF-ServerNetwork")

import protocol
import shipComponents
import universals
import shipSystem


class AccountComponent(object):
    address = None


class NetworkSystem(sandbox.UDPNetworkSystem):
    def init2(self):
        self.accept("broadcastData", self.broadcastData)
        self.accept("confirmPlayerStations", self.confirmPlayerStations)
        self.accept('playerDisconnected', self.playerDisconnected)
        self.activePlayers = []  # PlayerComponent
        self.playerMap = {} # {Address: Shipid}
        #self.shipMap = {} # {ShipID: {CONSOL: Netaddress}}
        #self.accept("shipGenerated", self.shipGenerated)
        if universals.runServer and not universals.runClient:
            sandbox.base.taskMgr.doMethodLater(0.2, self.sendShipUpdates, 'shipUpdates')

    def processPacket(self, msgID, remotePacketCount,
            ack, acks, hashID, serialized, address):
        #If not in our protocol range then we just reject
        if msgID < 0 or msgID > 200:
            return
        data = protocol.readProto(msgID, serialized)
        if data == None and msgID != protocol.LOGIN:
            log.error("Package reading error: " + str(msgID) + " " + serialized)
            return

        #Order of these will need to be optimized later
        if msgID == protocol.LOGIN:
            #TODO, if connection previously existed, reconnect
            #TODO: send current mission status.
            #TODO: Move ship select to separate function
            shipSys = sandbox.getSystem(shipSystem.ShipSystem)
            ackDatagram = protocol.shipClasses(shipSys.shipClasses)
            self.sendData(ackDatagram, address)
            ackDatagram = protocol.playerShipStations()
            self.sendData(ackDatagram, address)
            entity = sandbox.createEntity()
            component = AccountComponent()
            component.address = address
            entity.addComponent(component)
            self.activeConnections[component.address] = component
            print self.activeConnections
        elif msgID == protocol.REQUEST_STATIONS:
            entity = sandbox.entities[data.ship[0].id]
            info = entity.getComponent(shipComponents.InfoComponent)
            player = entity.getComponent(shipComponents.PlayerComponent)
            stations = data.ship[0].stations
            for stationName in universals.playerStations:
                if getattr(player, stationName) != 0:
                    print "Resend ship select window"
            sandbox.send('setPlayerStations', [address, data.ship[0].id, stations])
        elif msgID == protocol.SET_THROTTLE:
            sandbox.send('setThrottle', [self.playerMap[address], data])
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

    def sendShipUpdates(self, task):
        ships = sandbox.getSystem(shipSystem.ShipSystem).getPlayerShipEntities()
        ships += sandbox.getEntitiesByComponentType(shipComponents.AIPilotComponent)
        self.broadcastData(protocol.sendShipUpdates(ships))
        return task.again

    def playerDisconnected(self, address):
        del self.playerMap[address]

    def confirmPlayerStations(self, netAddress, shipid, stations):
        self.playerMap[netAddress] = shipid
        datagram = protocol.confirmStations(shipid, stations)
        self.sendData(datagram, netAddress)


class ClientComponent:
    """Theoretical component that stores which clients are
    also tracking this entity as well as last update"""
