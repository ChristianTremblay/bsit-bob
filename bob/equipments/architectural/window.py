from bob.connections.air import AirBidirectionalConnectionPoint
from bob.connections.electricity import OnOffSignalOutletConnectionPoint
from bob.connections.light import LightVisibleOutletConnectionPoint
from bob.core import BOB, P223, S223, Device, PropertyReference

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
