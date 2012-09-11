import sandbox
import DirectWindow
import boxes
from direct.gui.DirectGui import *

class GUISystem(sandbox.EntitySystem):
    def init(self):
        self.accept("shipSelectScreen", self.shipSelectScreen)

    def shipSelectScreen(self, db):
        guibox = boxes.HBox()
        leftbox = boxes.VBox()
        guibox.setScale(0.1)
        guibox.db = db
        ships = []
        for entityid in db:
            ships.append(db[entityid]['name'])
        guibox.reparentTo(sandbox.base.aspect2d)
        menu = DirectOptionMenu(text="options", items=ships)
        leftbox.pack(menu)
        
        
        guibox.pack(leftbox)
        rightbox = boxes.VBox()
        guibox.checkButtons = []
        for entityid in db:
            for station, status in db[entityid]['stations'].items():
                checkButton = DirectCheckButton(text=station)
                if status != 0:
                    checkButton['state'] = DGG.DISABLED
                rightbox.pack(checkButton)
                guibox.checkButtons.append(checkButton)
        guibox.pack(rightbox)
        button = DirectButton(text="Select", command=self.selectShip,
            extraArgs=[menu, db, guibox])
        guibox.pack(button)

    def selectShip(self, menu, db, guibox):
        name = menu.get()
        stations = []
        for entityid in db:
            if db[entityid]['name'] == name:
                for checkButton in guibox.checkButtons:
                    if checkButton['indicatorValue']:
                        stations.append(checkButton['text'])
        if not stations:
            return
        guibox.destroy()
        print stations
        sandbox.send('requestStations', [name, stations])