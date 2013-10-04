import sandbox

from direct.showbase import DirectObject
from pandac.PandaModules import CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionRay, GeomNode


#TODO: Move from base.cTrav to own system

class Picker(DirectObject.DirectObject):
    '''
    Mouse controller.
    '''
    def __init__(self):
        self.accept('makePickable', self.makePickable)
        self.accept('switchLevelRequest', self.switchLevel)
        self.level = 0
        #create traverser
        sandbox.pickTrav = CollisionTraverser()
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
        return

    def mouseLeft(self, pickedObj, pickedPoint):
        if pickedObj is None:
            sandbox.send('noSelected')
            return
        print "mouseLeft", pickedObj, pickedObj.getPos(), pickedPoint
        sandbox.send('mousePicked', [pickedObj])
        return

    def mousePick(self, but, queue):
        """mouse pick"""
        #get mouse coords
        if sandbox.base.mouseWatcherNode.hasMouse() is False:
            return
        mpos = sandbox.base.mouseWatcherNode.getMouse()
        #locate ray from camera lens to mouse coords
        self.ray.setFromLens(sandbox.base.camNode, mpos.getX(), mpos.getY())
        #get collision: picked obj and point
        pickedObj, pickedPoint = self.getCollision(queue)
        #call appropriate mouse function (left or right)
        if but == 1:
            self.mouseLeft(pickedObj, pickedPoint)
        if but == 3:
            self.mouseRight(pickedObj, pickedPoint)

    """Returns the picked nodepath and the picked 3d point"""
    def getCollision(self, queue):
        #do the traverse
        sandbox.pickTrav.traverse(sandbox.base.render)
        #process collision entries in queue
        if queue.getNumEntries() > 0:
            queue.sortEntries()
            for i in range(queue.getNumEntries()):
                collisionEntry = queue.getEntry(i)
                pickedObj = collisionEntry.getIntoNodePath()
                #iterate up in model hierarchy to found a pickable tag
                parent = pickedObj.getParent()
                for n in range(1):
                    #if parent.getTag('pickable') != "" or parent == render:
                    if parent.getPythonTag('pickable') != "" or parent == sandbox.base.render:
                        break
                    parent = parent.getParent()
                #return appropiate picked object
                #if parent.getTag('pickable') != "":
                if parent.getPythonTag('pickable') != "":
                    pickedObj = parent
                    pickedPoint = collisionEntry.getSurfacePoint(pickedObj)
                    #pickedNormal = collisionEntry.getSurfaceNormal(self.ancestor.worldNode)
                    #pickedDistance=pickedPoint.lengthSquared()#distance between your object and the collision
                    return pickedObj, pickedPoint
        return None, None

    def makePickable(self, newObj, tag='true'):
        """sets nodepath pickable state"""
        #newObj.setTag('pickable',tag)
        newObj.setPythonTag('pickable', tag)
        print "Pickable: ", newObj, "as", tag

    """creates a ray for detecting collisions"""
    def createRay(
        self, obj, ent, name, show=False, x=0, y=0, z=0, dx=0, dy=0, dz=-1
    ):
        #create queue
        obj.queue = CollisionHandlerQueue()
        #create ray
        obj.rayNP = ent.attachNewNode(CollisionNode(name))
        obj.ray = CollisionRay(x, y, z, dx, dy, dz)
        obj.rayNP.node().addSolid(obj.ray)
        obj.rayNP.node().setFromCollideMask(GeomNode.getDefaultCollideMask())
        sandbox.pickTrav.addCollider(obj.rayNP, obj.queue)
        if show:
            obj.rayNP.show()
