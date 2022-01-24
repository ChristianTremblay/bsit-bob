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
)
from ..signal import AnalogIn, AnalogOut

__namespace__ = s223

# Substances
class Water(Substance):
    pass


class DomesticWater(Water):
    pass


class DomesticHotWater(Water):
    pass


class ChilledWater(Water):
    pass


class HotWater(Water):
    pass


class CondensedWater(Water):
    pass


class GlycoledWater(Water):
    # glycol_proportion =
    pass


# Connections

# A class factory that would build everything ?
# lst_of_substance_classes = [HotWater, ChilledWater, ... ]
# for each in lst_of_substance_classes:


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
