from bob.connections.air import AirBidirectionalConnectionPoint
from bob.connections.light import LightVisibleOutletConnectionPoint
from bob.core import Device, PropertyReference, bob, s223

_namespace = bob


class Window(Device):
    _class_iri = s223.Window
    indoor: AirBidirectionalConnectionPoint
    outdoor: AirBidirectionalConnectionPoint
    naturalLight: LightVisibleOutletConnectionPoint

    # Those will come from something else, but be accessible from here.
    openCloseStatus: PropertyReference
    openCloseCommand: PropertyReference
    shadeStatus: PropertyReference
    shadeCommand: PropertyReference
    breakDetection: PropertyReference
