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

from pandac.PandaModules import *

from direct.directbase import DirectStart

parent = base.camera # render #
s = 0.8
l = 0.2

plightDummy = loader.loadModel('misc/sphere.egg')
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
render.setLight(alnp)

base.accept('w', base.toggleWireframe)


from shapeGenerator import *

# ------------------------------------------------------------------------------
# SAMPLES USAGE
# ------------------------------------------------------------------------------
tex = loader.loadTexture('testTex.png')
tex.setWrapU(Texture.WMRepeat)
tex.setWrapV(Texture.WMRepeat) #WMClamp)

r = .5
r2 = 0.25
h = 1

icosaeder = Icosaeder(r)
icosaeder.reparentTo(render)
icosaeder.setTexture(tex)
icosaeder.setPos(1.5,0,0)

cube = Cube(1,h,1)
cube.reparentTo(render)
cube.setTexture(tex)
cube.setPos(1.5,1.5,0)

pyramid = Pyramid(r)
pyramid.reparentTo(render)
pyramid.setTexture(tex)
pyramid.setPos(1.5,-1.5,0)


tube = Tube(r,r2, h)
tube.reparentTo(render)
tube.setTexture(tex)
tube.setPos(0,0,0)

capsule = Capsule(r, h)
capsule.reparentTo(render)
capsule.setTexture(tex)
capsule.setPos(0,1.5,0)

cylinder = Cylinder(r, h, 16)
cylinder.reparentTo(render)
cylinder.setTexture(tex)
cylinder.setPos(0,-1.5,0)

sphere = Sphere(-r, 128)
sphere.reparentTo(render)
sphere.setTexture(tex)
sphere.setPos(-1.5,0,0)



run()


