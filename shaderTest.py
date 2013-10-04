import direct.directbase.DirectStart
from panda3d.core import *

import shapeGenerator


render.setShaderAuto()

planet = shapeGenerator.Sphere(1, 64, 'planet')
planet.reparentTo(render)
#planet.setPos(5, 20, 0)

mesh = shapeGenerator.Sphere(1, 64, 'star')
mesh.reparentTo(render)
mesh.setPos(-5, 20, 0)


mesh.setShaderInput('time', 0)
shaders = Shader.load(Shader.SLGLSL, 'sphereVertex.glsl', 'starFrag2.glsl')
mesh.setShader(shaders)

run()
