from .core import (
    c223,
    Substance,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
    SystemInletConnectionPoint,
    SystemOutletConnectionPoint,
    Device,
)
from .signal import AnalogIn, AnalogOut

__namespace__ = c223


class Air(Substance):
    pass


class AirConnection(Connection):
    substance = Air.node_type


class AirConnectionPoint(ConnectionPoint):
    substance = Air.node_type


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    pass


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    pass


class AirSystemConnectionPoint(Air, SystemConnectionPoint):
    substance = Air.node_type


class AirInletSystemConnectionPoint(
    AirSystemConnectionPoint, SystemInletConnectionPoint
):
    pass


class AirOutletSystemConnectionPoint(
    AirSystemConnectionPoint, SystemOutletConnectionPoint
):
    pass


class Fan(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


class Damper(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position = AnalogOut


class Filter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    dp = AnalogOut


class AirFlowStation(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flow = AnalogIn


class Zone(Device):
    supplyAirInlet: AirInletConnectionPoint  # supply air goes in
    returnAirOutlet: AirOutletConnectionPoint  # return air goes out
