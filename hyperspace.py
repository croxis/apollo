from pandac.PandaModules import loadPrcFileData
loadPrcFileData('', 'frame-rate-meter-scale 0.035')
loadPrcFileData('', 'frame-rate-meter-side-margin 0.1')
loadPrcFileData('', 'show-frame-rate-meter 1')
loadPrcFileData('', 'window-title ' + "Hyperspace")
loadPrcFileData('', "sync-video 0")
loadPrcFileData("", "basic-shaders-only 0")
print "Video"

import sandbox
import universals

import math
import random

from panda3d.core import AmbientLight, VBase4, PerlinNoise2, PerlinNoise3
from panda3d.core import Texture, PNMImage, Filename, Shader
from panda3d.core import StackedPerlinNoise3, TextureStage, TexGenAttrib

'''VOXELS'''


sandbox.base.setBackgroundColor(0.0, 0.0, 0.0)

alight = AmbientLight('alight')
#alight.setColor(VBase4(0.5, 0.1, 0.1, 1))
alight.setColor(VBase4(1, 1, 1, 1))
alnp = sandbox.base.render.attachNewNode(alight)
sandbox.base.render.setLight(alnp)

skysphere = sandbox.base.loader.loadModel('sphere')
skysphere.setScale(-2000)
skysphere.reparentTo(sandbox.base.render)

tex = Texture('hyperspace clouds 1')
p = PNMImage(512, 512)



perm = range(256)
random.shuffle(perm)
perm += perm
dirs = [(math.cos(a * 2.0 * math.pi / 256),
         math.sin(a * 2.0 * math.pi / 256))
         for a in range(256)]

def noise(x, y, per):
    def surflet(gridX, gridY):
        distX, distY = abs(x-gridX), abs(y-gridY)
        polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
        polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
        hashed = perm[perm[int(gridX)%per] + int(gridY)%per]
        grad = (x-gridX)*dirs[hashed][0] + (y-gridY)*dirs[hashed][1]
        return polyX * polyY * grad
    intX, intY = int(x), int(y)
    return (surflet(intX+0, intY+0) + surflet(intX+1, intY+0) +
            surflet(intX+0, intY+1) + surflet(intX+1, intY+1))


def fBm(x, y, per, octs):
    val = 0
    for o in range(octs):
        val += 0.5**o * noise(x*2**o, y*2**o, per*2**o)
    return val

size, freq, octs, data = 128, 1/32.0, 5, []


p = PNMImage(128, 128)
for y in range(size):
    for x in range(size):
        #data.append(fBm(x*freq, y*freq, int(size*freq), octs))
        p.setXel(x, y, fBm(x*freq, y*freq, int(size*freq), octs))

#skysphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MEyeSphereMap)
tex.load(p)
skysphere.setTexture(tex)
'''skysphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
skysphere.setTexProjector(TextureStage.getDefault(), sandbox.base.render, skysphere)
skysphere.setTexPos(TextureStage.getDefault(), 0.5, 0.5, 0.5)
skysphere.setTexScale(TextureStage.getDefault(), 0.2)

''''''mesh = sandbox.base.loader.loadModel('ships/hyperion/hyperion')
mesh.setScale(0.001)
mesh.reparentTo(sandbox.base.render)''''''

#noise = PerlinNoise3(32, 32, 32, 256, 1)
noise = StackedPerlinNoise3(16, 16, 16, 3, 1, 0.5, 256, 1)
#noise = PerlinNoise3(32, 32, 32, 256)
#noise = PerlinNoise3()


def cosineInterpolate(a, b, x):
    ft = x * math.pi
    f = (1 - math.cos(ft)) * 0.5
    return a * (1 - f) + b * f


def smoothNoise(x, y, z):
    n = noise.noise(x, y, z)
    n += noise.noise(x - 1, y - 1, z - 1) / 4
    n += noise.noise(x + 1, y + 1, z + 1) / 4
    return n


def smoothNoise2D(x, y, z):
    corners = (noise.noise(x-1, y-1, z)+noise.noise(x+1, y-1, z)+noise.noise(x-1, y+1, z)+noise.noise(x+1, y+1, z)) / 16
    sides   = (noise.noise(x-1, y, z)  +noise.noise(x+1, y, z)  +noise.noise(x, y-1, z)  +noise.noise(x, y+1, z) ) /  8
    center  =  noise.noise(x, y, z) / 4
    return corners + sides + center


def pnoise(x, y, z):
    #return (smoothNoise2D(x, y, z) + 1) / 2.0
    return smoothNoise2D(x, y, z)


tex = Texture('hyperspace clouds 1')
tex.setup3dTexture()


for z in range(16):
    p = PNMImage(512, 512)
    for y in range(512):
        for x in range(512):
            #value = pnoise(x, y, universals.day)
            #value = noise.noise(x, y, universals.day)
            value = noise.noise(x, y, z)
            #value = smoothNoise2D(x, y, universals.day)
            #print value
            #p.setXel(x, y, (value, 0, 0))
            p.setXel(x, y, value)
    tex.load(p, z, 0)

#tex.load(p)

#tex.write(Filename('texture.png'))
#tex.write(Filename('woodgrain_#.png'), 0, 0, True, False)

#skysphere.setTexture(tex)
s = Shader.load(Shader.SLGLSL, "vert.glsl", "frag.glsl")
skysphere.setShader(s)'''

sandbox.run()
