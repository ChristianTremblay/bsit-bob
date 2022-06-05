from bob.connections.air import AirBidirectionalConnectionPoint
from bob.connections.light import LightVisibleOutletConnectionPoint
from bob.core import Device, PropertyReference, s223

_namespace = s223


class Door(Device):
    node_type = s223.Door
    door: AirBidirectionalConnectionPoint
    naturalLight: LightVisibleOutletConnectionPoint

    # Those will come from something else, but be accessible from here.
    openCloseStatus: PropertyReference
    openCloseCommand: PropertyReference
