import sandbox

from panda3d.core import Point3

import graphicsComponents
import shipComponents
import universals


class RenderSystem(sandbox.EntitySystem):
    def init(self):
        pass

    def begin(self):
        pass

    def process(self, entity):
        phys = entity.getComponent(shipComponents.BulletPhysicsComponent)
        gfx = entity.getComponent(graphicsComponents.RenderComponent)
        if entity.id is not universals.shipid:
            if universals.shipid is None:
                print "Void"
                return
            playerShip = sandbox.entities[universals.shipid]
            playerPhysics = playerShip.getComponent(shipComponents.BulletPhysicsComponent)
            diff = playerPhysics.nodePath.getPos() - phys.nodePath.getPos()
            gfx.mesh.setPos(Point3(0, 0, 0) - diff)
        #print phys.nodePath.getHpr()
        gfx.mesh.setHpr(phys.nodePath.getHpr())

    def end(self):
        pass
