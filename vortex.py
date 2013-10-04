from pandac.PandaModules import loadPrcFileData
loadPrcFileData('', 'frame-rate-meter-scale 0.035')
loadPrcFileData('', 'frame-rate-meter-side-margin 0.1')
loadPrcFileData('', 'show-frame-rate-meter 1')
loadPrcFileData('', 'window-title ' + "Vortex")
loadPrcFileData('', "sync-video 0")
loadPrcFileData('', 'task-timer-verbose 1')
loadPrcFileData('', 'pstats-tasks 1')
loadPrcFileData('', 'want-pstats 1')
loadPrcFileData('', 'framebuffer-stencil 1')
#loadPrcFileData('', 'show-buffers 1')
#loadPrcFileData('', 'notify-level-glgsg debug')

import sandbox

import shapeGenerator

from panda3d.core import AmbientLight, ColorWriteAttrib, NodePath, Shader, StencilAttrib, Vec4

# Set up stenciling system
stencilReader = StencilAttrib.make(1,StencilAttrib.SCFEqual,StencilAttrib.SOKeep,
                       StencilAttrib.SOKeep,StencilAttrib.SOKeep,1,1,0)

constantOneStencil = StencilAttrib.make(1,StencilAttrib.SCFAlways,StencilAttrib.SOZero,
                       StencilAttrib.SOReplace,StencilAttrib.SOReplace,1,0,1)

#mesh = shapeGenerator.Tube(0.18, 0.18, 5.0, 32)
# To be render on texture
#inside_vortex = shapeGenerator.ShellCylinder(-0.18, 5.0, 32)
inside_vortex = shapeGenerator.Circle(0.18, 32)
inside_vortex.node().setAttrib(constantOneStencil)
inside_vortex.node().setAttrib(ColorWriteAttrib.make(0))
inside_vortex.setBin('background', 0)
inside_vortex.setDepthWrite(0)

#inside_vortex.setH(180)
inside_vortex.setP(180)
#inside_vortex.setR(180)

vortex = shapeGenerator.ShellCylinder(-0.18, 10.0, 32)
vortex.node().setAttrib(stencilReader)
# Mask that fades out vortex
#outside_vortex = shapeGenerator.ShellCylinder(0.181, 0.05, 32)
outside_vortex = shapeGenerator.ShellCylinder(0.181, 5.0, 32)


def taskUpdate(task):
    #inside_vortex.setShaderInput('time', task.time/4.0)
    outside_vortex.setShaderInput('time', task.time/4.0)
    vortex.setShaderInput('time', task.time/4.0)
    #print base.camera.getPos()
    #print vortex_camera.getHpr()
    vortex_camera.setPos(sandbox.base.camera.getPos())
    vortex_camera.setHpr(sandbox.base.camera.getHpr())
    return task.cont

shaders = Shader.load(Shader.SLGLSL, 'vortex_vertex.glsl', 'vortex_fragment.glsl')
#inside_vortex.setShader(shaders)
outside_vortex.setShader(shaders)
vortex.setShader(shaders)

inside_vortex.reparentTo(sandbox.base.render)
#outside_vortex.reparentTo(sandbox.base.render)

sandbox.base.taskMgr.add(taskUpdate, "SpinCameraTask")

# Create buffers
vortex_buffer = sandbox.base.win.makeTextureBuffer("Vortex Buffer", 256, 256)
#vortex_texture = vortex_buffer.getTexture()
vortex_buffer.setSort(-100)
vortex_camera = sandbox.base.makeCamera(vortex_buffer)
vortex_scene = NodePath("Vortex Scene")
vortex_camera.reparentTo(vortex_scene)

#inside_vortex.setTexture(vortex_texture, 1)
#vortex.reparentTo(vortex_scene)
vortex.reparentTo(sandbox.base.render)

#alight = AmbientLight('alight')
#alnp = vortex_scene.attachNewNode(alight)
#alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
#vortex_scene.setLight(alnp)

def screenshot():
    sandbox.base.screenshot('/home/croxis/vortex/')

sandbox.base.accept("v", sandbox.base.bufferViewer.toggleEnable)
sandbox.base.accept("V", sandbox.base.bufferViewer.toggleEnable)

sandbox.base.accept("s", screenshot)


sandbox.run()
