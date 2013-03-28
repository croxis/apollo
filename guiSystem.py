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


'''Proposed UI
|---------------------------------------|
|           Station Menu bar            |
|---------------------------------------|
|   |                               |   |
|   |           Top Box             |   |
|   |-------------------------------|   |
|   |                               |   |
|   |                               |   |
|   |                               |   |
|   |          Center Box           |   |
|   |                               |   |
|   |                               |   |
|   |                               |   |
|   |                               |   |
|   |-------------------------------|   |
|   |          Bottom Box           |   |
|---------------------------------------|
Left box                        Right box'''


def debugView():
    fsm.request('Debug')


def navView():
    if fsm.state != 'Nav':
        log.info("Hard Switching to navigation UI")
        fsm.request('Nav')


def mainView():
    if fsm.state != 'MainScreen':
        log.info("Hard Switching to main screen UI")
        fsm.request('MainScreen')


def weaponsView():
    if fsm.state != 'Weapons':
        log.info("Hard Switching to weapons UI")
        fsm.request('Weapons')

bars = {}
text = {}
widgets = {}
tasks = {}
pick = picker.Picker()
stationButtons = []
stations = None


def buildBars():
    '''Builds or rebuilds gui bars to be populated by widgets'''
    for bar in bars:
        bars[bar].destroy()

    bars['stationBar'] = boxes.HBox()
    bars['stationBar'].setScale(0.1)
    global stationButtons
    stationButtons = []
    if stations:
        if stations.mainScreen:
            stationButtons.append(DirectButton(text="Main", command=mainView))
        if stations.navigation:
            stationButtons.append(DirectButton(text="Nav", command=navView))
        if stations.weapons:
            stationButtons.append(DirectButton(text="Weapons", command=weaponsView))
    stationButtons.append(DirectButton(text="DebugView", command=debugView))
    for station in stationButtons:
        bars['stationBar'].pack(station)
    
    #bars['stationBar'].pack(DirectButton(text="DebugView", command=debugView))
    #bars['stationBar'].pack(DirectButton(text="Nav", command=navView))
    #bars['stationBar'].pack(DirectButton(text="Main", command=mainView))
    #bars['stationBar'].pack(DirectButton(text="Weapons", command=weaponsView))
    bars['stationBar'].setPos(sandbox.base.a2dLeft, 0, sandbox.base.a2dTop)

    bars['leftBar'] = boxes.VBox()
    bars['leftBar'].setScale(0.1)
    bars['leftBar'].setPos(sandbox.base.a2dLeft, 0, 0.9)
    #stations.hide()

    bars['rightBar'] = boxes.VBox()
    bars['rightBar'].setScale(0.1)
    bars['rightBar'].setPos(sandbox.base.a2dRight, 0, 0.9)

    bars['topBar'] = boxes.HBox()
    bars['topBar'].setScale(0.1)
    bars['topBar'].setPos(-0.9, 0, 0.9)

    bars['bottomBar'] = boxes.HBox(margin=1)
    bars['bottomBar'].setScale(0.1)
    bars['bottomBar'].setPos(sandbox.base.a2dLeft, 0, sandbox.base.a2dBottom + 0.2)

    #Center bar as needed


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


def mainViewContext(item):
    base.camera.reparentTo(widgets['cameras'][item])
    base.camera.setPos(0, 0, 0)
    base.camera.setHpr(0, 0, 0)
    sandbox.send('showBG')


class GUIFSM(FSM):
    def __init__(self):
        FSM.__init__(self, 'GUIFSM')

    def enterStationSelect(self, playerShips):
        buildBars()
        bars['stationBar'].hide()
        shipBox = boxes.VBox()
        ships = [NEWSHIP]
        for playerShip in playerShips.ship:
            ships.append(playerShip.name)

        widgets['menu'] = DirectOptionMenu(
            text="options", items=ships,
            command=stationContext, initialitem=-1
        )
        shipBox.pack(widgets['menu'])

        widgets['shipName'] = DirectEntry(initialText="Ship Name here...")
        if playerShips.ship:
            widgets['shipName'].hide()
        shipBox.pack(widgets['shipName'])
        bars['topBar'].pack(shipBox)

        widgets['checkButtons'] = []
        stationBox = boxes.VBox()
        for playerShip in playerShips.ship:
            for stationName in universals.playerStations:
                checkButton = DirectCheckButton(text=stationName)
                if getattr(playerShip.stations, stationName):
                    checkButton['state'] = DGG.DISABLED
                stationBox.pack(checkButton)
                widgets['checkButtons'].append(checkButton)
        bars['topBar'].pack(stationBox)
        bars['topBar'].pack(
            DirectButton(
                text="Select", command=selectShip, extraArgs=[playerShips]
            )
        )
        return

    def exitStationSelect(self):
        bars['stationBar'].show()
        del widgets['menu']
        del widgets['checkButtons']
        del widgets['shipName']

    def enterDebug(self):
        buildBars()
        sandbox.send('debugView')
        sandbox.send('showBG')
        bars['stationBar'].show()

    def exitDebug(self):
        pass

    def enterNav(self):
        buildBars()
        sandbox.send('orthographic')
        sandbox.send('hideBG')
        text['xyz'] = OnscreenText(
            text="Standby", pos=(sandbox.base.a2dLeft, 0.85), scale=0.05,
            fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft, mayChange=1
        )
        text['localxyz'] = OnscreenText(
            text="Standby", pos=(sandbox.base.a2dLeft, 0.81), scale=0.05,
            fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft, mayChange=1
        )
        text['speed'] = OnscreenText(
            text="Standby", pos=(sandbox.base.a2dLeft, 0.77), scale=0.05,
            fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft, mayChange=1
        )
        bars['bottomBar'].pack(DirectLabel(text="Throttle"))
        widgets['throttle'] = DirectSlider(
            range=(-100, 100), value=0, pageSize=1, orientation=VERTICAL,
            frameSize=(-0.5, 0.5, -1, 1)
        )
        '''widgets['throttle'] = DirectScrollBar(
            range=(-100, 100), value=0, pageSize=1, orientation=VERTICAL
        )'''
        bars['bottomBar'].pack(widgets['throttle'])
        widgets['throt'] = 0

        bars['bottomBar'].pack(DirectLabel(text="Heading"))
        widgets['heading'] = DirectSlider(
            range=(-100, 100), value=0, pageSize=1, frameSize=(-1, 1, -0.5, 0.5)
        )
        bars['bottomBar'].pack(widgets['heading'])
        widgets['head'] = 0
        #widgets['stopHeading'] = DirectCheckButton(text="Stop Rotation")
        #bars['bottomBar'].pack(widgets['stopHeading'])
        #tasks['throttle'] = sandbox.base.taskMgr.doMethodLater(0.2, checkThrottle, 'throttle')

        texture = sandbox.base.loader.loadTexture("protractor.png")
        cm = CardMaker('protractor')
        widgets['protractor'] = sandbox.base.aspect2d.attachNewNode(cm.generate())
        widgets['protractor'].setTexture(texture)
        widgets['protractor'].setTransparency(TransparencyAttrib.MAlpha)
        widgets['protractor'].setPos(-0.75, 0, -0.75)
        widgets['protractor'].setScale(1.5)

    def exitNav(self):
        #sandbox.base.taskMgr.remove(tasks['throttle'])
        text['xyz'].removeNode()
        text['localxyz'].removeNode()
        text['speed'].removeNode()
        #widgets['throttle'].removeNode()
        #widgets['heading'].removeNode()
        widgets['protractor'].removeNode()
        del widgets['protractor']
        #del widgets['stopHeading']

    def enterMainScreen(self):
        buildBars()
        sandbox.send('perspective')
        sandbox.send('showBG')
        widgets['cameras'] = {}
        shipid = sandbox.getSystem(shipSystem.ShipSystem).shipid
        renderComponent = sandbox.entities[shipid].getComponent(graphicsComponents.RenderComponent)
        for joint in renderComponent.mesh.getJoints():
            if 'camera' in joint.getName().lower():
                #widgets['cameras'][joint.getName()] = joint
                widgets['cameras'][joint.getName()] = renderComponent.mesh.exposeJoint(None, "modelRoot", joint.getName())
        #print "Cameras", widgets['cameras']

        #DirectOptionMenu(text="options", items=ships, command=stationContext, initialitem=-1)
        widgets['cameraMenu'] = DirectOptionMenu(
            items=widgets['cameras'].keys(), command=mainViewContext
        )
        bars['topBar'].pack(widgets['cameraMenu'])

    def exitMainScreen(self):
        sandbox.base.camera.reparentTo(render)
        del widgets['cameras']
        del widgets['cameraMenu']

    def enterWeapons(self):
        buildBars()
        sandbox.send('orthographic')
        sandbox.send('hideBG')
        text['target'] = OnscreenText(
            text="Standby", pos=(sandbox.base.a2dLeft, 0.85), scale=0.05,
            fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft, mayChange=1
        )
        widgets['fire'] = DirectCheckButton(text="Fire at Will!")
        bars['bottomBar'].pack(widgets['fire'])

        '''texture = sandbox.base.loader.loadTexture("protractor.png")
        cm = CardMaker('protractor')
        widgets['protractor'] = sandbox.base.aspect2d.attachNewNode(cm.generate())
        widgets['protractor'].setTexture(texture)
        widgets['protractor'].setTransparency(TransparencyAttrib.MAlpha)
        widgets['protractor'].setPos(-0.75, 0, -0.75)
        widgets['protractor'].setScale(1.5)'''
        sandbox.send('hideBG')

    def exitWeapons(self):
        #sandbox.base.taskMgr.remove(tasks['throttle'])
        text['target'].removeNode()
        del text['target']
        widgets['fire'].destroy()
        del widgets['fire']


def selectShip(playerShips):
    name = widgets['menu'].get()
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
    #TODO: Switch to PID
    if widgets['stopHeading']["indicatorValue"]:
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
            widgets['heading']['value'] = 0
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
        buildBars()
        self.accept("shipSelectScreen", self.shipSelectScreen)
        self.accept("navigationScreen", self.navigationUI)
        self.accept("noSelected", self.noSelected)
        self.accept("mousePicked", self.mousePicked)
        self.accept("makeStationUI", self.makeStationUI)
        sandbox.base.taskMgr.add(self.autoTurnManager, "autoTurn")

    def begin(self):
        if fsm.state == 'Nav':
            if sandbox.getSystem(shipSystem.ShipSystem).shipid is not None:
                shipid = sandbox.getSystem(shipSystem.ShipSystem).shipid
                physics = sandbox.entities[shipid].getComponent(shipComponents.BulletPhysicsComponent)
                t = "X: " + str(round(physics.getTruePos().getX(), 1)) + ", Y: " + str(round(physics.getTruePos().getY(), 1)) + ", H: " + str(round(physics.nodePath.getH(), 1))
                text['xyz'].setText(t)
                localtext = "X: " + str(round(physics.nodePath.getX(), 1)) + ", Y: " + str(round(physics.nodePath.getY(), 1))
                text['localxyz'].setText(localtext)
                speedText = "Speed: " + str(round(physics.node.getLinearVelocity().length(), 1)) + " km/s"
                text['speed'].setText(speedText)

    def makeStationUI(self, data):
        global stations
        stations = data.stations
        stationButtons[0]['command']()
        #bars['stationBar'].pack(DirectButton(text="Nav", command=navView))
        #bars['stationBar'].pack(DirectButton(text="Main", command=mainView))
        #bars['stationBar'].pack(DirectButton(text="Weapons", command=weaponsView))

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

    def mousePicked(self, picked):
        print picked

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
