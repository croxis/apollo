'''from pandac.PandaModules import *

# ------------------------------------------------------------------------------
# SOME DEBUGGING STUFF
# ------------------------------------------------------------------------------
BORDER_SIZE          = 1.5
CARD_BACKGROUND_SIZE = Vec4(0.1, 0.2, 0.5, 0.1)
CARD_FRAME_SIZE      = Vec4(0.1, 0.1, 0.1, 0.1)
# colors of the border, background and text
BORDER_COLOR         = Vec4(0.3, 0.3, 0.3, 1.0)
BACKGROUND_COLOR     = Vec4(1.0, 1.0, 1.0, 0.7)
FONT_COLOR           = Vec4(0.0, 0.0, 0.0, 1.0)

class InfoText(NodePath):
  def __init__(self, parent):
    self.parent = parent

    NodePath.__init__(self, 'InfoTextNodePath')
    self.reparentTo(self.parent)

    # create the textnode
    self.textNode = TextNode('InfoTextNode')
    self.textNode.setTextColor(FONT_COLOR)
    self.textNodePath = NodePath.attachNewNode(self, self.textNode)

    # background of the textnode
    self.textNode.setCardColor(BACKGROUND_COLOR)
    self.textNode.setCardDecal(1) # required if in 3d space (z-fighting)
    self.textNode.setCardAsMargin(*CARD_BACKGROUND_SIZE) # left, right, bottom, top

    # frame of the textnode
    self.textNode.setFrameAsMargin(*(CARD_BACKGROUND_SIZE+CARD_FRAME_SIZE))
    self.textNode.setFrameLineWidth(BORDER_SIZE)
    self.textNode.setFrameColor(BORDER_COLOR)

    self.setText('default\ntext')

  def setText(self, text):
    self.textNode.setText(text)

class InfoTextBillaboarded(InfoText):
  def __init__(self, parent):
    # make the text viewing the camera
    self.billboardNodePath = parent.attachNewNode('InfoTextBillaboardedNode')
    self.billboardNodePath.setBillboardPointEye()
    #self.billboardNodePath.setZ(0.1)
    #self.billboardNodePath.setScale(.025)

    InfoText.__init__(self, self.billboardNodePath)

  def setText(self, text):
    InfoText.setText(self, text)

    # move the center of rotation to the lower left corner
    # this is not entirely correct, the x-coordinate is a bit too small
    frameSize = self.textNode.getFrameActual()
    pos = Vec3(frameSize.getX(),0,-frameSize.getZ()) # * NodePath.getScale(self, self.parent)
    self.textNodePath.setPos(self, pos)
'''
from pandac.PandaModules import loadPrcFileData

loadPrcFileData( '', 'frame-rate-meter-scale 0.035' )
loadPrcFileData( '', 'frame-rate-meter-side-margin 0.1' )
loadPrcFileData( '', 'show-frame-rate-meter 1' )
loadPrcFileData( '', 'window-title Atmosphere Demo' )
loadPrcFileData('', "sync-video 0") 

from pandac.PandaModules import *

from direct.directbase import DirectStart
from direct.task import Task
from panda3d.core import Shader, PointLight
import math
#base.setBackgroundColor(0.0, 0.0, 0.0) 

parent = base.camera # render #
s = 0.8
l = 0.2

'''plightDummy = loader.loadModel('misc/sphere.egg')
plightDummy.reparentTo(parent)
plightDummy.setPos(10,-10,10) # right top
plight = PointLight('plight')
plight.setColor(VBase4(s, l, l, 1))
plnp = plightDummy.attachNewNode(plight)
render.setLight(plnp)

plightDummy = loader.loadModel('misc/sphere.egg')
plightDummy.reparentTo(parent)
plightDummy.setPos(10,-10,-10) # right bottom
plight = PointLight('plight')
plight.setColor(VBase4(l, s, l, 1))
plnp = plightDummy.attachNewNode(plight)
render.setLight(plnp)

plightDummy = loader.loadModel('misc/sphere.egg')
plightDummy.reparentTo(parent)
plightDummy.setPos(-10,-10,0) # left
plight = PointLight('plight')
plight.setColor(VBase4(l, l, s, 1))
plnp = plightDummy.attachNewNode(plight)
render.setLight(plnp)

alight = AmbientLight('alight')
alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
alnp = parent.attachNewNode(alight)
render.setLight(alnp)'''

base.accept('w', base.toggleWireframe)


from shapeGenerator import *

# ------------------------------------------------------------------------------
# SAMPLES USAGE
# ------------------------------------------------------------------------------
tex = loader.loadTexture('testTex.png')
tex.setWrapU(Texture.WMRepeat)
tex.setWrapV(Texture.WMRepeat) #WMClamp)

r = 1
r2 = 0.25
h = 1

light = render.attachNewNode( PointLight( "sunPointLight" ) )
light.setPos(1000,0,0)
render.setLight( light )
sun = Sphere(r, 128)
sun.reparentTo(render)
sun.setPos(1050,0,0)

earth = Sphere(r, 128)
earth.reparentTo(render)
earth.setTexture(tex)

atmo = Sphere(-r*1.025, 128)
atmo.reparentTo(render)

print earth.radius, atmo.radius

outerRadius = -atmo.radius
scale = 1/(outerRadius - earth.radius)

atmo.setShaderInput("fOuterRadius", outerRadius)
atmo.setShaderInput("fInnerRadius", earth.radius)
atmo.setShaderInput("fOuterRadius2", outerRadius * outerRadius)
atmo.setShaderInput("fInnerRadius2", earth.radius * earth.radius)

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

atmoShader = Shader.load("shader.cg")
atmo.setShader(atmoShader)

def shaderUpdate(task):
    atmo.setShaderInput("v3CameraPos", base.camera.getPos().getX(),
        base.camera.getPos().getY(),
        base.camera.getPos().getZ())
    atmo.setShaderInput("fCameraHeight", base.camera.getPos().length())
    print base.camera.getPos().length()
    atmo.setShaderInput("fCameraHeight2", base.camera.getPos().length()*base.camera.getPos().length())
    print "yup"
    return task.cont

taskMgr.add(shaderUpdate, 'shaderUpdate') 

run()


