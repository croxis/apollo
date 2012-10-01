from pandac.PandaModules import loadPrcFileData

loadPrcFileData( '', 'frame-rate-meter-scale 0.035' )
loadPrcFileData( '', 'frame-rate-meter-side-margin 0.1' )
loadPrcFileData( '', 'show-frame-rate-meter 1' )
loadPrcFileData( '', 'window-title Atmosphere Demo' )
loadPrcFileData('', "sync-video 0")

from direct.directbase.DirectStart import *
from direct.task import Task
from panda3d.core import Shader, PointLight
import math

from shapeGenerator import *
base.setBackgroundColor(0.0, 0.0, 0.0)

light = render.attachNewNode( PointLight( "sunPointLight" ) )
light.setPos(1000,0,0)
render.setLight( light )
sun = loader.loadModel("models/solar_sky_sphere")
sun.reparentTo(render)
sun.setPos(1050,0,0)
sun.setScale(5)

#earth = loader.loadModel("models/planet_sphere")
earth = Sphere(1, 128)
earth.reparentTo(render)

# This is a sphere with the normals flipped
#atmo = loader.loadModel("models/solar_sky_sphere")
atmo = Sphere(-1, 128)
#atmo.reparentTo(earth)
atmo.reparentTo(render)
atmo.setScale(1.025)


#outerRadius = abs((earth.getScale().getX() * atmo.getScale().getX()))   # ?????
outerRadius = atmo.getScale().getX()
scale = 1/(outerRadius - earth.getScale().getX())
atmo.setShaderInput("fOuterRadius", outerRadius)
atmo.setShaderInput("fInnerRadius", earth.getScale().getX())
atmo.setShaderInput("fOuterRadius2", outerRadius * outerRadius)
atmo.setShaderInput("fInnerRadius2", earth.getScale().getX() * earth.getScale().getX())

atmo.setShaderInput("fKr4PI", 0.000055 * 4 * 3.14159)
atmo.setShaderInput("fKm4PI", 0.000015 * 4 * 3.14159)

atmo.setShaderInput("fScale", scale)
atmo.setShaderInput("fScaleDepth", 0.25)
atmo.setShaderInput("fScaleOverScaleDepth", scale/0.25)

# Currently hardcoded in shader
atmo.setShaderInput("fSamples", 10.0)
atmo.setShaderInput("nSamples", 10)

# These do sunsets and sky colors
# Brightness of sun
ESun = 15
# Reyleight Scattering (Main sky colors)
atmo.setShaderInput("fKrESun", 0.000055 * ESun)
# Mie Scattering -- Haze and sun halos
atmo.setShaderInput("fKmESun", 0.000015 * ESun)
# Color of sun
atmo.setShaderInput("v3InvWavelength", 1.0 / math.pow(0.650, 4),
                                  1.0 / math.pow(0.570, 4),
                                  1.0 / math.pow(0.465, 4))
                                 
atmo.setShaderInput("v3CameraPos", base.camera.getPos().getX(),
        base.camera.getPos().getY(),
        base.camera.getPos().getZ())
# Light vector from center of planet.       
lightv = light.getPos()
lightdir = lightv / lightv.length()

atmo.setShaderInput("v3LightPos", lightdir[0], lightdir[1], lightdir[2])
     
atmo.setShaderInput("fCameraHeight", base.camera.getPos().length())
atmo.setShaderInput("fCameraHeight2", base.camera.getPos().length()*base.camera.getPos().length())

atmo.setShaderInput("g", 0.90)
atmo.setShaderInput("g2", 0.81)
atmo.setShaderInput("float", 2)

atmoShader = Shader.load("atmo.cg")
atmo.setShader(atmoShader)

def shaderUpdate(task):
    atmo.setShaderInput("v3CameraPos", base.camera.getPos().getX(),
        base.camera.getPos().getY(),
        base.camera.getPos().getZ())
    atmo.setShaderInput("fCameraHeight", base.camera.getPos().length())
    atmo.setShaderInput("fCameraHeight2", base.camera.getPos().length()*base.camera.getPos().length())
    return task.cont

taskMgr.add(shaderUpdate, 'shaderUpdate')
run() 