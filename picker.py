import sandbox

import math

from direct.showbase import DirectObject
from pandac.PandaModules import CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionRay, GeomNode


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
        if base.mouseWatcherNode.hasMouse() == False:
            return
        mpos = sandbox.base.mouseWatcherNode.getMouse()
        #locate ray from camera lens to mouse coords
        self.ray.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        #get collision: picked obj and point
        pickedObj, pickedPoint = self.getCollision(self.queue)
        #call appropiate mouse function (left or right)
        if pickedObj == None:
            return
        cell = (int(math.floor(pickedPoint[0])), int(math.floor(pickedPoint[1])))
        return cell

    def mousePick(self, but, queue):
        """mouse pick"""
        #print "Mousepick"
        #get mouse coords
        if base.mouseWatcherNode.hasMouse() == False:
            return
        mpos = base.mouseWatcherNode.getMouse()
        #locate ray from camera lens to mouse coords
        self.ray.setFromLens(base.camNode, mpos.getX(), mpos.getY())
        #get collision: picked obj and point
        pickedObj, pickedPoint = self.getCollision(queue)
        #call appropiate mouse function (left or right)
        if but == 1:
            self.mouseLeft(pickedObj, pickedPoint)
        if but == 3:
            self.mouseRight(pickedObj, pickedPoint)

    """Returns the picked nodepath and the picked 3d point"""
    def getCollision(self, queue):
        #do the traverse
        base.cTrav.traverse(render)
        #process collision entries in queue
        if queue.getNumEntries() > 0:
            queue.sortEntries()
            for i in range(queue.getNumEntries()):
                collisionEntry = queue.getEntry(i)
                pickedObj = collisionEntry.getIntoNodePath()
                #iterate up in model hierarchy to found a pickable tag
                parent = pickedObj.getParent()
                for n in range(1):
                    if parent.getTag('pickable') != "" or parent == render:
                        break
                    parent = parent.getParent()
                #return appropiate picked object
                if parent.getTag('pickable') != "":
                    pickedObj = parent
                    pickedPoint = collisionEntry.getSurfacePoint(pickedObj)
                    #pickedNormal = collisionEntry.getSurfaceNormal(self.ancestor.worldNode)
                    #pickedDistance=pickedPoint.lengthSquared()#distance between your object and the collision
                    return pickedObj, pickedPoint
        return None, None

    def makePickable(self,newObj,tag='true'):
        """sets nodepath pickable state"""
        newObj.setTag('pickable',tag)
        #print "Pickable: ",newObj,"as",tag
    
    """creates a ray for detecting collisions"""
    def createRay(self,obj,ent,name,show=False,x=0,y=0,z=0,dx=0,dy=0,dz=-1):
        #create queue
        obj.queue = CollisionHandlerQueue()
        #create ray  
        obj.rayNP=ent.attachNewNode(CollisionNode(name))
        obj.ray=CollisionRay(x,y,z,dx,dy,dz)
        obj.rayNP.node().addSolid(obj.ray)
        obj.rayNP.node().setFromCollideMask(GeomNode.getDefaultCollideMask())
        base.cTrav.addCollider(obj.rayNP, obj.queue) 
        if show: obj.rayNP.show()