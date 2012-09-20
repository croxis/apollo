import sandbox
#import DirectWindow
import boxes
import graphicsComponents
import shipComponents
import shipSystem
import universals
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import VERTICAL
from pandac.PandaModules import Spotlight,PerspectiveLens,Fog,OrthographicLens
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import TextNode


class GUISystem(sandbox.EntitySystem):
    def init(self):
        self.accept("shipSelectScreen", self.shipSelectScreen)
        self.accept("navigationScreen", self.navigationUI)
        self.mode = ''
        self.text = {}

    def begin(self):
        if self.mode == 'navigation':
            if sandbox.getSystem(shipSystem.ShipSystem).shipid != None:
                shipid = sandbox.getSystem(shipSystem.ShipSystem).shipid
                physics = sandbox.entities[shipid].getComponent(shipComponents.BulletPhysicsComponent)
                text = "X: " + str(round(physics.nodePath.getX(), 1)) + ", Y: " + str(round(physics.nodePath.getY(), 1)) + ", H: " + str(round(physics.nodePath.getH(), 1))
                self.text['xyz'].setText(text)
                speedText = "Speed: " + str(round(physics.node.getLinearVelocity().length(), 1)) + " km/s"
                self.text['speed'].setText(speedText)
                gfx = sandbox.entities[shipid].getComponent(graphicsComponents.RenderComponent)
                gfx.mesh.setPos(physics.nodePath.getPos())
                gfx.mesh.setHpr(physics.nodePath.getHpr())

    def shipSelectScreen(self, playerShips):
        guibox = boxes.HBox()
        leftbox = boxes.VBox()
        guibox.setScale(0.1)
        guibox.db = playerShips
        ships = []
        for playerShip in playerShips.ship:
            ships.append(playerShip.name)
        guibox.reparentTo(sandbox.base.aspect2d)
        menu = DirectOptionMenu(text="options", items=ships)
        leftbox.pack(menu)
        guibox.pack(leftbox)
        rightbox = boxes.VBox()
        guibox.checkButtons = []
        for playerShip in playerShips.ship:
            for stationName in universals.playerStations:
                checkButton = DirectCheckButton(text=stationName)
                if getattr(playerShip.stations, stationName):
                    checkButton['state'] = DGG.DISABLED
                rightbox.pack(checkButton)
                guibox.checkButtons.append(checkButton)
        guibox.pack(rightbox)
        button = DirectButton(text="Select", command=self.selectShip,
            extraArgs=[menu, playerShips, guibox])
        guibox.pack(button)

    def selectShip(self, menu, playerShips, guibox):
        name = menu.get()
        stations = []
        entityID = 0
        for playerShip in playerShips.ship:
            if playerShip.name == name:
                entityID = playerShip.id
                for checkButton in guibox.checkButtons:
                    if checkButton['indicatorValue']:
                        stations.append(checkButton['text'])
        if not stations:
            return
        guibox.destroy()
        sandbox.send('requestStations', [entityID, stations])

    def navigationUI(self):
        self.mode = 'navigation'
        #sandbox.base.disableMouse()
        #sandbox.base.camera.setPos(0, 0, 5000)
        #sandbox.base.camera.setHpr(0, -90, 0)
        lens = OrthographicLens()
        lens.setFilmSize(2000)
        #sandbox.base.cam.node().setLens(lens)
        self.text['xyz'] = OnscreenText(text="Standby", pos=(-0.95, 0.95),
            scale=0.07, fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter, mayChange=1)
        self.text['speed'] = OnscreenText(text="Standby", pos=(-0.95, 0.9),
            scale=0.07, fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter, mayChange=1)
        throttlebox = boxes.VBox()
        throttlebox.setScale(0.1)
        throttlebox.setPos(-1, 0, -0.75)
        throttleLable = DirectLabel(text="Throttle")
        throttlebox.pack(throttleLable)
        '''self.throttle = DirectSlider(range=(-100, 100), value=0,
            pageSize=1, command=self.setThrottle, orientation=VERTICAL)'''
        self.throttle = DirectSlider(range=(-100, 100), value=0,
            pageSize=1, orientation=VERTICAL)
        throttlebox.pack(self.throttle)
        self.throt = 0

        headingbox = boxes.VBox()
        headingbox.setScale(0.1)
        headingbox.setPos(0, 0, -0.75)
        headingLable = DirectLabel(text="Heading")
        headingbox.pack(headingLable)
        '''self.throttle = DirectSlider(range=(-100, 100), value=0,
            pageSize=1, command=self.setThrottle, orientation=VERTICAL)'''
        self.heading = DirectSlider(range=(-100, 100), value=0,
            pageSize=1)
        headingbox.pack(self.heading)
        self.head = 0

        sandbox.base.taskMgr.doMethodLater(0.2, self.checkThrottle, 'throttle')

    def checkThrottle(self, task):
        if self.throt != self.throttle['value'] or self.head != self.heading['value']:
            self.throt = self.throttle['value']
            self.head = self.heading['value']
            sandbox.send("requestThrottle", [self.throttle['value'], self.heading['value']])
        return task.again
