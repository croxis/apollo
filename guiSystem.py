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
from direct.showbase import DirectObject
from pandac.PandaModules import CollisionTraverser,CollisionHandlerQueue,CollisionNode,CollisionRay,GeomNode

from panda3d.core import Point3, TextNode
import math


def convertPos(point):
    return Point3(point.getX(), point.getY(), point.getZ())


class GUISystem(sandbox.EntitySystem):
    def init(self):
        self.accept("shipSelectScreen", self.shipSelectScreen)
        self.accept("navigationScreen", self.navigationUI)
        self.mode = ''
        self.text = {}
        self.picker = Picker()

    def begin(self):
        if self.mode == 'navigation':
            if sandbox.getSystem(shipSystem.ShipSystem).shipid != None:
                shipid = sandbox.getSystem(shipSystem.ShipSystem).shipid
                physics = sandbox.entities[shipid].getComponent(shipComponents.BulletPhysicsComponent)
                text = "X: " + str(round(physics.getTruePos().getX(), 1)) + ", Y: " + str(round(physics.getTruePos().getY(), 1)) + ", H: " + str(round(physics.nodePath.getH(), 1))
                self.text['xyz'].setText(text)
                localtext = "X: " + str(round(physics.nodePath.getX(), 1)) + ", Y: " + str(round(physics.nodePath.getY(), 1))
                self.text['localxyz'].setText(localtext)
                speedText = "Speed: " + str(round(physics.node.getLinearVelocity().length(), 1)) + " km/s"
                self.text['speed'].setText(speedText)

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
        self.text['xyz'] = OnscreenText(text="Standby", pos=(-1, 0.95),
            scale=0.06, fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft, mayChange=1)
        self.text['localxyz'] = OnscreenText(text="Standby", pos=(-1, 0.9),
            scale=0.06, fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft, mayChange=1)
        self.text['speed'] = OnscreenText(text="Standby", pos=(-1, 0.85),
            scale=0.06, fg=(1, 0.5, 0.5, 1), align=TextNode.ALeft, mayChange=1)
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


class Picker(DirectObject.DirectObject):
    '''
    Mouse controller.
    '''
    def __init__(self):
        self.accept('makePickable', self.makePickable)
        self.accept('switchLevelRequest', self.switchLevel)
        self.level = 0
        #create traverser
        base.cTrav = CollisionTraverser()
        #create collision ray
        self.createRay(self, sandbox.base.camera, name="mouseRay", show=True)
        #initialize mousePick
        #self.accept('mouse1-up', self.mousePick, [1,self.queue])
        self.accept('mouse1', self.mousePick, [1, self.queue])
        #initialize mouseRightPick
        #self.accept('mouse3', self.mousePick, [3, self.queue])

    def switchLevel(self, level):
        self.level = level

    def mouseRight(self, pickedObj, pickedPoint):
        contextDict = {}
        if pickedObj == None:
            pass
        else:
            #get cell from pickedpoint
            cell = (int(math.floor(pickedPoint[0])), int(math.floor(pickedPoint[1])), self.level)
            contextDict['cell'] = cell
        messenger.send('buildContextMenu', [contextDict])

    def mouseLeft(self, pickedObj, pickedPoint):
        if pickedObj == None:
            print "No object clicked on"
            return
        print "mouseLeft", pickedObj, pickedObj.getPos(), pickedPoint
        return
        cell = (int(math.floor(pickedPoint[0])), int(math.floor(pickedPoint[1])), self.level)
        #print cell
        if database.terrain[cell[2]][cell[0]][cell[1]]['structure']:
            messenger.send('structureClick', [cell, ])

    def getMouseCell(self):
        """Returns terrain cell coordinates (x,y) at mouse pointer"""
        #get mouse coords
        if base.mouseWatcherNode.hasMouse()==False: return
        mpos=base.mouseWatcherNode.getMouse()
        #locate ray from camera lens to mouse coords
        self.ray.setFromLens(base.camNode, mpos.getX(),mpos.getY())
        #get collision: picked obj and point
        pickedObj,pickedPoint=self.getCollision(self.queue)
        #call appropiate mouse function (left or right)
        if pickedObj==None:  return
        cell=(int(math.floor(pickedPoint[0])),int(math.floor(pickedPoint[1])))
        return cell  

    def mousePick(self, but, queue):
        """mouse pick""" 
        #print "Mousepick"
        #get mouse coords
        if base.mouseWatcherNode.hasMouse()==False: return
        mpos=base.mouseWatcherNode.getMouse()
        #locate ray from camera lens to mouse coords
        self.ray.setFromLens(base.camNode, mpos.getX(),mpos.getY())
        #get collision: picked obj and point
        pickedObj,pickedPoint=self.getCollision(queue)
        #call appropiate mouse function (left or right)
        if but==1:self.mouseLeft(pickedObj,pickedPoint)
        if but==3:self.mouseRight(pickedObj,pickedPoint)

    """Returns the picked nodepath and the picked 3d point"""
    def getCollision(self, queue):
        #do the traverse
        base.cTrav.traverse(render)
        #process collision entries in queue
        if queue.getNumEntries() > 0:
            queue.sortEntries()
            for i in range(queue.getNumEntries()):
                collisionEntry=queue.getEntry(i)
                pickedObj=collisionEntry.getIntoNodePath()
                #iterate up in model hierarchy to found a pickable tag
                parent=pickedObj.getParent()
                for n in range(1):
                    if parent.getTag('pickable')!="" or parent==render: break
                    parent=parent.getParent()
                #return appropiate picked object
                if parent.getTag('pickable')!="":
                    pickedObj=parent
                    pickedPoint = collisionEntry.getSurfacePoint(pickedObj)
                    #pickedNormal = collisionEntry.getSurfaceNormal(self.ancestor.worldNode)
                    #pickedDistance=pickedPoint.lengthSquared()#distance between your object and the collision
                    return pickedObj,pickedPoint         
        return None,None

    def makePickable(self,newObj,tag='true'):
        """sets nodepath pickable state"""
        newObj.setTag('pickable',tag)
        #print "Pickable: ",newObj,"as",tag
    
    """creates a ray for detecting collisions"""
    def createRay(self,obj,ent,name,show=False,x=0,y=0,z=0,dx=0,dy=0,dz=-1):
        #create queue
        obj.queue=CollisionHandlerQueue()
        #create ray  
        obj.rayNP=ent.attachNewNode(CollisionNode(name))
        obj.ray=CollisionRay(x,y,z,dx,dy,dz)
        obj.rayNP.node().addSolid(obj.ray)
        obj.rayNP.node().setFromCollideMask(GeomNode.getDefaultCollideMask())
        base.cTrav.addCollider(obj.rayNP, obj.queue) 
        if show: obj.rayNP.show()