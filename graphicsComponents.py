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
