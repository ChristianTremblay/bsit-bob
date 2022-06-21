from bob.connections.air import AirBidirectionalConnectionPoint
from bob.connections.light import LightVisibleOutletConnectionPoint
from bob.core import Device, PropertyReference, BOB, S223

_namespace = BOB


class Door(Device):
    _class_iri = S223.Door
    door: AirBidirectionalConnectionPoint
    naturalLight: LightVisibleOutletConnectionPoint

    # Those will come from something else, but be accessible from here.
    openCloseStatus: PropertyReference
    openCloseCommand: PropertyReference
