from panda3d.core import PerlinNoise2


class CameraComponent(object):
    pass


class RenderComponent(object):
    mesh = None
    visible = True


class PlanetRender(object):
    body = None
    atmosphere = None


class StarRender(object):
    body = None
    atmosphere = None
    light = None
    noise = PerlinNoise2(64, 64)
    noise_texture = None
