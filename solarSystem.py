"""Stuff needed for running a solar system"""
from math import sin, cos, radians, degrees, sqrt, atan2

import sandbox
import yaml

from direct.stdpy.file import *
from panda3d.core import LPoint3d, NodePath, Point3, PointLight, Shader
from panda3d.core import Texture, TextureStage,  TexGenAttrib

import graphicsComponents
import shapeGenerator
import universals

#from pandac.PandaModules import loadPrcFileData
#loadPrcFileData("", "notify-level-ITF-SolarSystem debug")
from direct.directnotify.DirectNotify import DirectNotify
log = DirectNotify().newCategory("ITF-SolarSystem")

'''Types of bodies:
    solid: Planet, asteroid
    star: Star
    moon: moon (due to orbit information)'''

TYPES = {'moon': 0, 'solid': 1, 'star': 2, 'barycenter': 3}


class BaryCenter(NodePath):
    '''This class is used to simulate the center of a multibody system.
    Mass is the sum of masses of the multibody system
    SOI is the sphere of influence of a body for patched conics
    In this case soi is the "virtual" sphere for the entire system'''


class Body(BaryCenter):
    period = 0
    radius = 1
    kind = "solid"


class Star(Body):
    kind = "star"
    absoluteM = 1
    spectralType = ""


class CelestialComponent(object):
    nodePath = None
    truePos = LPoint3d(0, 0, 0)
    mass = 0
    soi = 0
    kind = None
    orbit = {}


class SolarSystemSystem(sandbox.EntitySystem):
    """Generates celestial bodies and moves them in orbit"""
    def getBodyPosition(self, entity, time):
        """Returns celestial position relative to the parent"""
        # Convert to radians
        M = radians(eval(entity.orbit['M'])(time))
        w = radians(eval(entity.orbit['w'])(time))
        i = radians(eval(entity.orbit['i'])(time))
        N = radians(eval(entity.orbit['N'])(time))
        a = entity.orbit['a']
        e = eval(entity.orbit['e'])(time)
        # Compute eccentric anomaly
        E = M + e * sin(M) * (1.0 + e * cos(M))
        if degrees(E) > 0.05:
            E = self.computeE(E, M, e)
        # http://stjarnhimlen.se/comp/tutorial.html
        # Compute distance and true anomaly
        xv = a * (cos(E) - e)
        yv = a * (sqrt(1.0 - e * e) * sin(E))
        v = atan2(yv, xv)
        r = sqrt(xv * xv + yv * yv)
        xh = r * (cos(N) * cos(v + w) - sin(N) * sin(v + w) * cos(i))
        yh = r * (sin(N) * cos(v + w) + cos(N) * sin(v + w) * cos(i))
        zh = r * (sin(v + w) * sin(i))
        position = LPoint3d(xh, yh, zh)
        # If we are not a moon then our orbits are done in au.
        # Our units in panda are km, so we convert to km
        # FIXME: Add moon body type
        if entity.kind != TYPES['moon']:
            position = position * 149598000
        return position

    def get2DBodyPosition(self, entity, time):
        """Returns celestial position relative to the parent"""
        # Convert to radians
        M = radians(eval(entity.orbit['M'])(time))
        w = radians(eval(entity.orbit['w'])(time))
        i = radians(eval(entity.orbit['i'])(time))
        N = radians(eval(entity.orbit['N'])(time))
        a = entity.orbit['a']
        e = eval(entity.orbit['e'])(time)
        # Compute eccentric anomaly
        E = M + e * sin(M) * (1.0 + e * cos(M))
        if degrees(E) > 0.05:
            E = self.computeE(E, M, e)
        # Compute distance and true anomaly
        xv = a * (cos(E) - e)
        yv = a * (sqrt(1.0 - e * e) * sin(E))
        v = atan2(yv, xv)
        r = sqrt(xv * xv + yv * yv)
        xh = r * (cos(N) * cos(v + w) - sin(N) * sin(v + w) * cos(i))
        yh = r * (sin(N) * cos(v + w) + cos(N) * sin(v + w) * cos(i))
        position = LPoint3d(xh, yh, 0)
        # If we are not a moon then our orbits are done in au.
        # We need to convert to km
        # FIXME: Add moon body type
        if entity.kind != TYPES['moon']:
            position = position * 149598000
        return position

    def computeE(self, E0, M, e):
        '''Iterative function for a higher accuracy of E'''
        E1 = E0 - (E0 - e * sin(E0) - M) / (1 - e * cos(E0))
        if abs(abs(degrees(E1)) - abs(degrees(E0))) > 0.001:
            E1 = self.computeE(E1, M, e)
        return E1

    def process(self, entity):
        '''Gets the xyz position of the body, relative to its parent, on the given day before/after the date of element. Units will be in AU'''
        #Static bodies for now
        #universals.day += globalClock.getDt() / 86400 * universals.TIMEFACTOR
        component = entity.getComponent(CelestialComponent)
        if component.orbit:
            #print component.nodePath, self.get2DBodyPosition(component.nodePath, universals.day)
            #component.nodePath.setPos(self.get2DBodyPosition(component, universals.day))
            component.truePos = self.get2DBodyPosition(component, universals.day)

    def init(self, name='Sol'):
        log.debug("Loading Solar System Bodies")
        stream = file("solarsystem.yaml", "r")
        self.bodies = []
        solarDB = yaml.load(stream)
        stream.close()
        #self.sphere = shapeGenerator.Sphere(1, 128)
        #self.solarSystemRoot = NodePath(name)
        for bodyName, bodyDB in solarDB[name].items():
            self.generateNode(bodyName, bodyDB, universals.solarSystemRoot)

    def generateNode(self, name, DB, parentNode):
        log.debug("Setting up " + name)
        bodyEntity = sandbox.createEntity()
        component = CelestialComponent()
        if DB['type'] == 'solid':
            body = Body(name)
        elif DB['type'] == 'moon':
            body = Body(name)
            body.kind = "moon"
        elif DB['type'] == 'star':
            body = Star(name)
            body.absoluteM = DB['absolute magnitude']
            body.spectral = DB['spectral']
        elif DB['type'] == 'barycenter':
            body = BaryCenter(name)

        component.kind = TYPES[DB['type']]

        if DB['type'] != "barycenter":
            component.mass = DB['mass']
            body.radius = DB['radius']
            body.rotation = DB['rotation']

        if 'orbit' in DB:
            component.orbit = DB['orbit']
            body.period = DB['period']
            #body.setPos(self.get2DBodyPosition(component, universals.day))
            component.truePos = self.get2DBodyPosition(component, universals.day)
            if name == "Earth":
                universals.spawn = component.truePos + LPoint3d(6771, 0, 0)

        if parentNode == universals.solarSystemRoot:
            universals.defaultSOIid = bodyEntity.id
            component.soi = 0
        elif DB['type'] != 'star' or DB['type'] != 'barycenter':
            component.soi = self.getSOI(component.mass, self.bodies[0].mass, component.orbit['a'])

        body.type = DB['type']
        body.reparentTo(parentNode)
        component.nodePath = body
        self.bodies.append(component)
        bodyEntity.addComponent(component)

        if universals.runClient and DB['type'] == 'star':
            component = graphicsComponents.RenderComponent()
            component.mesh = NodePath(name)
            #self.sphere.copyTo(component.mesh)
            component.mesh = shapeGenerator.Sphere(body.radius, 128)
            #component.mesh.setScale(body.radius)
            component.mesh.reparentTo(sandbox.base.render)
            texture = sandbox.base.loader.loadTexture('planets/' + DB['texture'])
            texture.setMinfilter(Texture.FTLinearMipmapLinear)
            component.mesh.setTexture(texture, 1)
            component.light = sandbox.base.render.attachNewNode(PointLight("sunPointLight"))
            render.setLight(component.light)

        if universals.runClient and (DB['type'] == 'solid' or DB['type'] == 'moon'):
            component = graphicsComponents.RenderComponent()
            component.mesh = shapeGenerator.Sphere(body.radius, 128)
            #component.mesh.setScale(body.radius)
            component.mesh.reparentTo(render)
            if '#' in DB['texture']:
                component.mesh.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
                component.mesh.setTexProjector(TextureStage.getDefault(), sandbox.base.render, component.mesh)
                component.mesh.setTexScale(TextureStage.getDefault(), 1,  1, -1)
                component.mesh.setTexHpr(TextureStage.getDefault(), 90, -18, 90)
                #self.mesh.setHpr(0, 90, 0)
                texture = loader.loadCubeMap('planets/' + DB['texture'])
            else:
                texture = sandbox.base.loader.loadTexture('planets/' + DB['texture'])
            #texture.setMinfilter(Texture.FTLinearMipmapLinear)
            component.mesh.setTexture(texture, 1)
            '''if "atmosphere" in DB:
                component.atmosphere = shapeGenerator.Sphere(-1, 128)
                component.atmosphere.reparentTo(render)
                component.atmosphere.setScale(body.radius * 1.025)
                outerRadius = component.atmosphere.getScale().getX()
                scale = 1 / (outerRadius - component.body.getScale().getX())
                component.atmosphere.setShaderInput("fOuterRadius", outerRadius)
                component.atmosphere.setShaderInput("fInnerRadius", component.mesh.getScale().getX())
                component.atmosphere.setShaderInput("fOuterRadius2", outerRadius * outerRadius)
                component.atmosphere.setShaderInput("fInnerRadius2",
                    component.mesh.getScale().getX()
                    * component.mesh.getScale().getX())

                component.atmosphere.setShaderInput("fKr4PI",
                    0.000055 * 4 * 3.14159)
                component.atmosphere.setShaderInput("fKm4PI",
                    0.000015 * 4 * 3.14159)

                component.atmosphere.setShaderInput("fScale", scale)
                component.atmosphere.setShaderInput("fScaleDepth", 0.25)
                component.atmosphere.setShaderInput("fScaleOverScaleDepth", scale / 0.25)

                # Currently hard coded in shader
                component.atmosphere.setShaderInput("fSamples", 10.0)
                component.atmosphere.setShaderInput("nSamples", 10)
                # These do sunsets and sky colors
                # Brightness of sun
                ESun = 15
                # Reyleight Scattering (Main sky colors)
                component.atmosphere.setShaderInput("fKrESun", 0.000055 * ESun)
                # Mie Scattering -- Haze and sun halos
                component.atmosphere.setShaderInput("fKmESun", 0.000015 * ESun)
                # Color of sun
                component.atmosphere.setShaderInput("v3InvWavelength", 1.0 / math.pow(0.650, 4),
                                                  1.0 / math.pow(0.570, 4),
                                                  1.0 / math.pow(0.465, 4))
                #component.atmosphere.setShader(Shader.load("atmo.cg"))'''
            bodyEntity.addComponent(component)
        log.info(name + " set Up")

        if 'bodies' in DB:
            for bodyName, bodyDB in DB['bodies'].items():
                self.generateNode(bodyName, bodyDB, body)

    def getSOI(self, massPlanet, massSun, axis):
        '''Calculates the sphere of influence of a body for patch conic approximation'''
        return axis * (massPlanet / massSun) ** (2 / 5.0)

    """def getBodyComponents(self):
        '''Returns only planets and moons. Assumes single star starsystem'''
        bodies = []
        bodies += sandbox.getComponents(Body)
        return bodies

    def getBodyEntities(self):
        '''Returns only planets and moons. Assumes single star starsystem'''
        bodies = []
        bodies += sandbox.getEntitiesByComponentType(Body)
        return bodies"""
