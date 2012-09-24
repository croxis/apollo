"""Stuff needed for running a solar system"""
from math import sin, cos, radians, degrees, sqrt, atan2

import sandbox
import yaml

from direct.stdpy.file import *
from panda3d.core import NodePath, Point3

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
        # http:#stjarnhimlen.se/comp/tutorial.html
        # Compute distance and true anomaly
        xv = a * (cos(E) - e)
        yv = a * (sqrt(1.0 - e * e) * sin(E))
        v = atan2(yv, xv)
        r = sqrt(xv * xv + yv * yv)
        xh = r * (cos(N) * cos(v + w) - sin(N) * sin(v + w) * cos(i))
        yh = r * (sin(N) * cos(v + w) + cos(N) * sin(v + w) * cos(i))
        zh = r * (sin(v + w) * sin(i))
        position = Point3(xh, yh, zh)
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
        # http:#stjarnhimlen.se/comp/tutorial.html
        # Compute distance and true anomaly
        xv = a * (cos(E) - e)
        yv = a * (sqrt(1.0 - e * e) * sin(E))
        v = atan2(yv, xv)
        r = sqrt(xv * xv + yv * yv)
        xh = r * (cos(N) * cos(v + w) - sin(N) * sin(v + w) * cos(i))
        yh = r * (sin(N) * cos(v + w) + cos(N) * sin(v + w) * cos(i))
        position = Point3(xh, yh, 0)
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
            component.nodePath.setPos(self.get2DBodyPosition(component, universals.day))

    def init(self, name='Sol'):
        log.debug("Loading Solar System Bodies")
        stream = file("solarsystem.yaml", "r")
        self.bodies = []
        solarDB = yaml.load(stream)
        stream.close()
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
            body.setPos(self.get2DBodyPosition(component, universals.day))

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
