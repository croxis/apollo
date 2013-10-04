import sandbox
import shapeGenerator

from panda3d.core import PerlinNoise2, PNMImage, PointLight, Shader, Texture, Vec3, Vec4
from direct.filter.CommonFilters import CommonFilters

#sandbox.base.render.setShaderAuto()

planet = shapeGenerator.Sphere(1, 64, 'planet')
planet.reparentTo(sandbox.base.render)

planet.setPos(5, 20, 0)

mesh = shapeGenerator.Sphere(1, 64, 'star')
mesh.reparentTo(sandbox.base.render)

mesh.setPos(-5, 20, 0)

noise = PerlinNoise2(64, 64)
texture = Texture('noise')
texture.setup2dTexture()
img = PNMImage(1024, 1024)
for y in range(1024):
    for x in range(1024):
        img.setXel(x, y, noise.noise(x, y))
texture.load(img)
mesh.setTexture(texture, 1)

mesh.setShaderInput('time', 0)
#shaders = Shader.load(Shader.SLGLSL, 'vortexVertex.glsl', 'starFrag2.glsl')
shaders = Shader.load(Shader.SLGLSL, 'sphereVertex.glsl', 'starFrag2.glsl')
mesh.setShader(shaders)

light = mesh.attachNewNode(PointLight("sun"))
light.node().setColor(Vec4(1, 1, 1, 1))
sandbox.base.render.setLight(light)


def time_update(task):
    mesh.setShaderInput('time', task.time)
    mesh.setH(-task.time*10)
    return task.cont


sandbox.base.taskMgr.add(time_update, 'task')

#filters = CommonFilters(base.win, base.cam)
#filters.setBloom()

sandbox.run()
