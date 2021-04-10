from rdflib import URIRef
from .core import (
    s223,
    Substance,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    Device,
)
from .signal import AnalogIn, AnalogOut

__namespace__ = s223


class Air(Substance):
    pass

class AirConnection(Connection):
    hasSubstance: URIRef = Air.node_type
    node_type = None


class AirConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = Air.node_type
    node_type = None


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    node_type = None


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    node_type = None


class AirSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance: URIRef = Air.node_type
    node_type = None


class AirInletSystemConnectionPoint(
    AirSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class AirOutletSystemConnectionPoint(
    AirSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


class Electricity(Substance):
    pass

class PowerConnection(Connection):
    hasSubstance = Electricity.node_type
    node_type = None

class PowerConnectionPoint(ConnectionPoint):
    hasSubstance = Electricity.node_type
    node_type = None

class PowerInletConnectionPoint(InletConnectionPoint, PowerConnectionPoint):
    node_type = None

class PowerOutletConnectionPoint(OutletConnectionPoint, PowerConnectionPoint):
    node_type = None

class ElectricalSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance = Electricity.node_type
    node_type = None


class HotWater(Substance):
    pass


class HotWaterConnection(Connection):
    hasSubstance = HotWater.node_type
    node_type = None


class HotWaterConnectionPoint(ConnectionPoint):
    hasSubstance = HotWater.node_type
    node_type = None


class HotWaterInletConnectionPoint(InletConnectionPoint, HotWaterConnectionPoint):
    node_type = None


class HotWaterOutletConnectionPoint(OutletConnectionPoint, HotWaterConnectionPoint):
    node_type = None


class HotWaterSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance = HotWater.node_type
    node_type = None


class HotWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    node_type = None


class HotWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    node_type = None

class ChilledWater(Substance):
    pass


class ChilledWaterConnection(Connection):
    hasSubstance = ChilledWater.node_type
    node_type = None


class ChilledWaterConnectionPoint(ConnectionPoint):
    hasSubstance = ChilledWater.node_type
    node_type = None


class ChilledWaterInletConnectionPoint(
    InletConnectionPoint, ChilledWaterConnectionPoint
):
    node_type = None


class ChilledWaterOutletConnectionPoint(
    OutletConnectionPoint, ChilledWaterConnectionPoint
):
    node_type = None


class ChilledWaterSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance = ChilledWater.node_type
    node_type = None


class ChilledWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    node_type = None


class ChilledWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    node_type = None


class ChilledWaterValve(Device):
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint
    position = AnalogIn


class ChilledWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint