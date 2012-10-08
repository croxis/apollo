import sandbox

import math

from panda3d.core import OrthographicLens, PerspectiveLens, Point3

import graphicsComponents
import shapeGenerator
import shipComponents
import solarSystem
import universals

PERSPECTIVE = True


def orthographic():
    global PERSPECTIVE
    PERSPECTIVE = False
    sandbox.base.disableMouse()
    sandbox.base.camera.setPos(0, 0, 3000)
    sandbox.base.camera.setHpr(0, -90, 0)
    lens = OrthographicLens()
    lens.setFilmSize(10)
    sandbox.base.cam.node().setLens(lens)


def perspective():
    global PERSPECTIVE
    PERSPECTIVE = True
    sandbox.base.enableMouse()
    lens = PerspectiveLens()
    sandbox.base.cam.node().setLens(lens)


def convertPos(point):
    return Point3(point.getX(), point.getY(), point.getZ())


class RenderSystem(sandbox.EntitySystem):
    def init(self):
        self.skybox = shapeGenerator.Sphere(-50000, 128, 'Skysphere')
        texture = sandbox.base.loader.loadTexture('galaxy.jpg')
        self.skybox.setTexture(texture, 1)
        self.skybox.reparentTo(sandbox.base.render)
        self.accept('hideBG', self.hideBG)
        self.accept('showBG', self.showBG)
        self.accept('perspective', perspective)
        self.accept('orthographic', orthographic)

    def hideBG(self):
        self.skybox.hide()

    def showBG(self):
        self.skybox.show()

    def begin(self):
        pass

    def process(self, entity):
        if entity.hasComponent(shipComponents.BulletPhysicsComponent):
            phys = entity.getComponent(shipComponents.BulletPhysicsComponent)
            pos = phys.getTruePos()
        elif entity.hasComponent(solarSystem.CelestialComponent):
            phys = entity.getComponent(solarSystem.CelestialComponent)
            pos = phys.truePos
        gfx = entity.getComponent(graphicsComponents.RenderComponent)
        if entity.id is not universals.shipid:
            if universals.shipid is None:
                return
            playerShip = sandbox.entities[universals.shipid]
            playerPhysics = playerShip.getComponent(shipComponents.BulletPhysicsComponent)
            diff = playerPhysics.getTruePos() - pos
            #near = sandbox.base.camLens.getFar() / 2.0
            scale = 1.0 / math.sqrt(diff.length())
            #if gfx.mesh.getName() == "Sol":
            #    print "Sol", gfx.mesh.getScale()
            #TODO: LOD sphers to some other sort. Imposters maybe?
            #if scale < 0.001:
            #    scale = 0.001
            if not PERSPECTIVE:
                diff = diff * scale
                gfx.mesh.setPos(Point3(0, 0, 0) - convertPos(diff))
                gfx.mesh.setScale(scale)
            '''if diff.length() > near:
                x = diff.length() - near
                scale = 1.0 / math.sqrt(x)
            else:
                gfx.mesh.setPos(Point3(0, 0, 0) - convertPos(diff))'''
        #print phys.nodePath.getHpr()
        gfx.mesh.setHpr(phys.nodePath.getHpr())

    def end(self):
        pass
