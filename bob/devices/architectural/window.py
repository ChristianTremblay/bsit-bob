from bob.connections.air import AirBidirectionalConnectionPoint
from bob.connections.light import LightVisibleOutletConnectionPoint
from bob.core import Device, PropertyReference, BOB, S223, P223

_namespace = BOB


class Window(Device):
    _class_iri = P223.Window
    indoor: AirBidirectionalConnectionPoint
    outdoor: AirBidirectionalConnectionPoint
    naturalLight: LightVisibleOutletConnectionPoint

    # Those will come from something else, but be accessible from here.
    openCloseStatus: PropertyReference
    openCloseCommand: PropertyReference
    shadeStatus: PropertyReference
    shadeCommand: PropertyReference
    breakDetection: PropertyReference
