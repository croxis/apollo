import sandbox

import math

from panda3d.core import OrthographicLens, PerspectiveLens, Point3

import graphicsComponents
import shapeGenerator
import shipComponents
import solarSystem
import universals

PERSPECTIVE = True

MIN_FILM_SIZE = 5


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
    sandbox.base.disableMouse()
    lens = PerspectiveLens()
    sandbox.base.cam.node().setLens(lens)


def debug():
    global PERSPECTIVE
    PERSPECTIVE = True
    sandbox.base.cam.setPos(0, 0, 0)
    sandbox.base.enableMouse()
    lens = PerspectiveLens()
    sandbox.base.cam.node().setLens(lens)


def wheel_up():
    if not PERSPECTIVE:
        if sandbox.base.cam.node().getLens().getFilmSize()[0] >= MIN_FILM_SIZE:
            sandbox.base.cam.node().getLens().setFilmSize(sandbox.base.cam.node().getLens().getFilmSize() - 1)


def wheel_down():
    if not PERSPECTIVE:
        sandbox.base.cam.node().getLens().setFilmSize(sandbox.base.cam.node().getLens().getFilmSize() + 1)


def convertPos(point):
    return Point3(point.getX(), point.getY(), point.getZ())


class RenderSystem(sandbox.EntitySystem):
    def init(self):
        #self.skybox = shapeGenerator.Sphere(-50000, 128, 'Skysphere')
        self.skybox = shapeGenerator.Sphere(-50000, 64, 'Skysphere')
        texture = sandbox.base.loader.loadTexture('galaxy.jpg')
        self.skybox.setTexture(texture, 1)
        self.skybox.reparentTo(sandbox.base.render)
        self.accept('hideBG', self.hideBG)
        self.accept('showBG', self.showBG)
        self.accept('perspective', perspective)
        self.accept('orthographic', orthographic)
        self.accept('debugView', debug)
        self.accept('wheel_up', wheel_up)
        self.accept('wheel_down', wheel_down)

    def hideBG(self):
        self.skybox.hide()

    def showBG(self):
        self.skybox.show()

    def begin(self):
        pass

    def process(self, entity):
        scaleFactor = 1
        if entity.hasComponent(shipComponents.BulletPhysicsComponent):
            phys = entity.getComponent(shipComponents.BulletPhysicsComponent)
            pos = phys.getTruePos()
            scaleFactor = universals.CONVERT  # Convert ship meshes, in meters, to engine units
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
            scale = 1.0 / math.sqrt(diff.length())
            if PERSPECTIVE:
                diff = diff * scale
                gfx.mesh.setPos(Point3(0, 0, 0) - convertPos(diff))
                gfx.mesh.setScale(scale)
                if entity.hasComponent(solarSystem.CelestialComponent):
                    gfx.mesh.setScale(scale)
                else:
                    gfx.mesh.setScale(scale / scaleFactor)
            else:
                gfx.mesh.setPos(Point3(0, 0, 0) - convertPos(diff))
                if entity.hasComponent(solarSystem.CelestialComponent):
                    gfx.mesh.setScale(1)
                else:
                    gfx.mesh.setScale(1.0 / scaleFactor)


            #near = sandbox.base.camLens.getFar() / 2.0
            '''scale = 1.0 / math.sqrt(diff.length()) / scaleFactor

            #if gfx.mesh.getName() == "Sol":
            #    print "Sol", gfx.mesh.getScale()
            #TODO: LOD sphers to some other sort. Imposters maybe?
            #if scale < 0.001:
            #    scale = 0.001
            if not PERSPECTIVE:
                diff = diff * scale
                gfx.mesh.setPos(Point3(0, 0, 0) - convertPos(diff))
            else:
                diff = diff * scale
                gfx.mesh.setPos(Point3(0, 0, 0) - convertPos(diff))'''

            '''if diff.length() > near:
                x = diff.length() - near
                scale = 1.0 / math.sqrt(x)
            else:
                gfx.mesh.setPos(Point3(0, 0, 0) - convertPos(diff))'''
        #print phys.nodePath.getHpr()
        gfx.mesh.setHpr(phys.nodePath.getHpr())

    def end(self):
        pass
