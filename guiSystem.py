import sandbox
#import DirectWindow
import boxes
import universals
from direct.gui.DirectGui import *


class GUISystem(sandbox.EntitySystem):
    def init(self):
        self.accept("shipSelectScreen", self.shipSelectScreen)

    def shipSelectScreen(self, playerShips):
        guibox = boxes.HBox()
        leftbox = boxes.VBox()
        guibox.setScale(0.1)
        guibox.db = playerShips
        print playerShips, dir(playerShips)
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
