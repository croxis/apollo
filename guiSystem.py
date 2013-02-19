import math

import sandbox
import sandbox.mathextra

import boxes
import graphicsComponents
import picker
import pid
import shipComponents
import shipSystem
import universals

from direct.fsm.FSM import FSM
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import VERTICAL
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import CardMaker, Point3, TextNode, TransparencyAttrib

from direct.directnotify.DirectNotify import DirectNotify
log = DirectNotify().newCategory("ITF-GUISystem")


NEWSHIP = 'New ship...'


def debugView():
    fsm.request('Debug')


def navView():
    if fsm.state != 'Nav':
        log.info("Hard Switching to navigation UI")
        fsm.request('Nav')


text = {}
widgets = {}
tasks = {}
stations = boxes.HBox()
stations.setScale(0.1)
stations.pack(DirectButton(text="DebugView", command=debugView))
stations.pack(DirectButton(text="Nav", command=navView))
stations.setPos(sandbox.base.a2dLeft, 0, sandbox.base.a2dTop)
stations.hide()

pick = picker.Picker()


def convertPos(point):
    return Point3(point.getX(), point.getY(), point.getZ())


def stationContext(item):
    if item == NEWSHIP:
        widgets['shipName'].show()
        for widget in widgets['checkButtons']:
            widget.hide()
    else:
        widgets['shipName'].hide()
        for widget in widgets['checkButtons']:
            widget.show()


class GUIFSM(FSM):
    def __init__(self):
        FSM.__init__(self, 'GUIFSM')

    def enterStationSelect(self, playerShips):
        stations.hide()
        widgets['guibox'] = boxes.HBox()
        leftbox = boxes.VBox()
        widgets['guibox'].setScale(0.1)
        widgets['guibox'].db = playerShips
        ships = [NEWSHIP]
        for playerShip in playerShips.ship:
            ships.append(playerShip.name)
        widgets['guibox'].reparentTo(sandbox.base.aspect2d)
        menu = DirectOptionMenu(text="options", items=ships, command=stationContext, initialitem=-1)
        widgets['menu'] = menu
        leftbox.pack(menu)
        widgets['guibox'].pack(leftbox)
        rightbox = boxes.VBox()
        widgets['checkButtons'] = []
        shipName = DirectEntry(initialText="Ship Name here...")
        if playerShips.ship:
            shipName.hide()
        widgets['shipName'] = shipName
        rightbox.pack(shipName)
        for playerShip in playerShips.ship:
            for stationName in universals.playerStations:
                checkButton = DirectCheckButton(text=stationName)
                if getattr(playerShip.stations, stationName):
                    checkButton['state'] = DGG.DISABLED
                rightbox.pack(checkButton)
                widgets['checkButtons'].append(checkButton)
        widgets['guibox'].pack(rightbox)
        button = DirectButton(text="Select", command=selectShip,
            extraArgs=[menu, playerShips])
        widgets['guibox'].pack(button)
        widgets['guibox'].setPos(-1, 0, 0.5)

    def exitStationSelect(self):
        widgets['guibox'].destroy()
        del widgets['guibox']
        del widgets['menu']
        del widgets['checkButtons']
        del widgets['shipName']

    def enterDebug(self):
        stations.show()
        sandbox.send('perspective')
        sandbox.send('showBG')

    def exitDebug(self):
        pass

    def enterNav(self):
        stations.show()
        sandbox.send('orthographic')
        text['xyz'] = OnscreenText(text="Standby", pos=(sandbox.base.a2dLeft, 0.85),
            scale=0.05, fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft, mayChange=1)
        text['localxyz'] = OnscreenText(text="Standby", pos=(sandbox.base.a2dLeft, 0.81),
            scale=0.05, fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft, mayChange=1)
        text['speed'] = OnscreenText(text="Standby", pos=(sandbox.base.a2dLeft, 0.77),
            scale=0.05, fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft, mayChange=1)
        throttlebox = boxes.VBox()
        throttlebox.setScale(0.1)
        throttlebox.setPos(-1, 0, -0.75)
        throttleLable = DirectLabel(text="Throttle")
        throttlebox.pack(throttleLable)
        widgets['throttle'] = DirectSlider(range=(-100, 100), value=0,
            pageSize=1, orientation=VERTICAL, frameSize=(-0.5, 0.5, -1, 1))
        throttlebox.pack(widgets['throttle'])
        widgets['throt'] = 0

        headingbox = boxes.VBox()
        headingbox.setScale(0.1)
        headingbox.setPos(0, 0, -0.75)
        headingLable = DirectLabel(text="Heading")
        headingbox.pack(headingLable)
        widgets['heading'] = DirectSlider(range=(-100, 100), value=0,
            pageSize=1, frameSize=(-1, 1, -0.5, 0.5))
        headingbox.pack(widgets['heading'])
        widgets['head'] = 0
        #stopHeading = DirectCheckButton(text="Stop Rotation")
        #headingbox.pack(stopHeading)
        #widgets['stopHeading'] = stopHeading
        tasks['throttle'] = sandbox.base.taskMgr.doMethodLater(0.2, checkThrottle, 'throttle')

        texture = sandbox.base.loader.loadTexture("protractor.png")
        cm = CardMaker('protractor')
        widgets['protractor'] = sandbox.base.aspect2d.attachNewNode(cm.generate())
        widgets['protractor'].setTexture(texture)
        #widgets['protractor'].setTransparency(TransparencyAttrib.MBinary)
        widgets['protractor'].setTransparency(TransparencyAttrib.MAlpha)
        widgets['protractor'].setPos(-0.75, 0, -0.75)
        widgets['protractor'].setScale(1.5)
        sandbox.send('makePickable', [widgets['protractor']])
        sandbox.send('hideBG')

    def exitNav(self):
        pass
        #text['xyz'].removeNode()
        #text['localxyz'].removeNode()
        #text['speed'].removeNode()
        #widgets['throttle'].removeNode()
        #widgets['heading'].removeNode()
        widgets['protractor'].removeNode()
        del widgets['protractor']
        #del widgets['stopHeading']
        #sandbox.base.taskMgr.remove(tasks['throttle'])


def selectShip(menu, playerShips):
    name = menu.get()
    if name == NEWSHIP:
        sandbox.send('requestCreateShip', [widgets['shipName'].get(), 'Hyperion'])
        return
    stations = []
    entityID = 0
    for playerShip in playerShips.ship:
        if playerShip.name == name:
            entityID = playerShip.id
            for checkButton in widgets['checkButtons']:
                if checkButton['indicatorValue']:
                    stations.append(checkButton['text'])
    if not stations:
        return
    sandbox.send('requestStations', [entityID, stations])


def checkThrottle(task):
    shipid = sandbox.getSystem(shipSystem.ShipSystem).shipid
    physicsComponent = sandbox.entities[shipid].getComponent(shipComponents.BulletPhysicsComponent)
    '''if widgets['stopHeading']["indicatorValue"]:
        heading = 100
        if abs(physicsComponent.node.getAngularVelocity()[2]) < 0.5:
            heading = 50
        if abs(physicsComponent.node.getAngularVelocity()[2]) < 0.1:
            heading = 25
        if abs(physicsComponent.node.getAngularVelocity()[2]) < 0.01:
            heading = 0
            widgets['stopHeading']["indicatorValue"] = True
            widgets['stopHeading'].setIndicatorValue()
        if physicsComponent.node.getAngularVelocity()[2] > 0:
            widgets['heading']['value'] = heading
        elif physicsComponent.node.getAngularVelocity()[2] < 0:
            widgets['heading']['value'] = -heading
        else:
            widgets['heading']['value'] = 0'''
    if widgets['throt'] != widgets['throttle']['value'] or widgets['head'] != widgets['heading']['value']:
        widgets['throt'] = widgets['throttle']['value']
        widgets['head'] = widgets['heading']['value']
        sandbox.send("requestThrottle", [widgets['throttle']['value'], widgets['heading']['value']])
    return task.again


fsm = GUIFSM()


class GUISystem(sandbox.EntitySystem):
    #TODO: Change autoturning into a component
    autoTurn = False
    autoTurnTarget = 0
    autoTurnPID = pid.PID()
    lastPError = 0.0

    def init(self):
        self.accept("shipSelectScreen", self.shipSelectScreen)
        self.accept("navigationScreen", self.navigationUI)
        self.accept("noSelected", self.noSelected)
        sandbox.base.taskMgr.add(self.autoTurnManager, "autoTurn")

    def begin(self):
        if fsm.state == 'Nav':
            if sandbox.getSystem(shipSystem.ShipSystem).shipid != None:
                shipid = sandbox.getSystem(shipSystem.ShipSystem).shipid
                physics = sandbox.entities[shipid].getComponent(shipComponents.BulletPhysicsComponent)
                t = "X: " + str(round(physics.getTruePos().getX(), 1)) + ", Y: " + str(round(physics.getTruePos().getY(), 1)) + ", H: " + str(round(physics.nodePath.getH(), 1))
                text['xyz'].setText(t)
                localtext = "X: " + str(round(physics.nodePath.getX(), 1)) + ", Y: " + str(round(physics.nodePath.getY(), 1))
                text['localxyz'].setText(localtext)
                speedText = "Speed: " + str(round(physics.node.getLinearVelocity().length(), 1)) + " km/s"
                text['speed'].setText(speedText)

    def shipSelectScreen(self, playerShips):
        fsm.request('StationSelect', playerShips)

    def navigationUI(self):
        if fsm.state != 'Nav':
            log.info("Switching to navigation UI")
            fsm.request('Nav')

    def noSelected(self):
        if fsm.state == 'Nav':
            #x = sandbox.base.mouseWatcherNode.getMouseX()
            #y = sandbox.base.mouseWatcherNode.getMouseY()
            x = sandbox.base.mouseWatcherNode.getMouseY()
            y = -sandbox.base.mouseWatcherNode.getMouseX()
            # Rotate to screen coordinate system
            if x != 0:
                angle = math.degrees(math.atan2(y, x))  # - 90
            else:
                angle = 0
            if angle < 0:
                angle += 360
            shipid = sandbox.getSystem(shipSystem.ShipSystem).shipid
            physics = sandbox.entities[shipid].getComponent(shipComponents.BulletPhysicsComponent)
            currentAngle = physics.nodePath.getH() % 360
            trueDifference = abs(currentAngle - angle)
            distance = 180 - abs(trueDifference - 180)
            self.autoTurn = True
            self.autoTurnTarget = angle
            print math.degrees(math.atan2(y, x)), angle, currentAngle, trueDifference, distance

    def autoTurnManager(self, task):
        if self.autoTurn:
            shipid = sandbox.getSystem(shipSystem.ShipSystem).shipid
            physicsComponent =\
                sandbox.entities[shipid].getComponent(shipComponents.BulletPhysicsComponent)
            currentAngle = physicsComponent.nodePath.getH() % 360

            directionDistance =\
                sandbox.mathextra.signedAngularDistance(self.autoTurnTarget,
                currentAngle)

            #print currentAngle, self.autoTurnTarget, trueDifference, distance, directionDistance
            #print currentAngle, self.autoTurnTarget, directionDistance

            #angularVelocity = physicsComponent.node.getAngularVelocity()

            #self.autoTurnPID.UpdateP(error, position)
            #self.autoTurnPID.UpdateI(error, position)
            #self.autoTurnPID.UpdateD(error, position)

            # Gaines -- tuned experimentally
            Kp = 10 ** 2 * (2 / 5.0 * physicsComponent.node.getMass() * 1 ** 2)
            Ki = 0
            Kd = 2 * 10 * (2 / 5.0 * physicsComponent.node.getMass() * 1 ** 2)

            #pError = self.autoTurnTarget - currentAngle
            pError = directionDistance
            iError = pError * globalClock.getDt()
            dError = (pError - self.lastPError) / globalClock.getDt()

            self.lastPError = pError

            torque = Kp * pError + Ki * iError + Kd * dError
            #print "Calculated Torque:", torque, currentAngle, self.autoTurnTarget, directionDistance
            heading = sandbox.mathextra.clamp(torque, -100, 100)
            widgets['heading']['value'] = -heading
        return task.cont


def sameSign(x, y):
    '''Fun little function that returns if two variables are the same sign'''
    return ((x < 0) == (y < 0))
