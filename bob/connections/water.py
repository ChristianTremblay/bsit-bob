from rdflib import URIRef
from ..core import s223, p223

from ..core import (
    Medium,
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

# Medium
class Water(Medium):
    node_type: URIRef = s223["Medium-Water"]


class DomesticWater(Water):
    node_type: URIRef = s223["Water-DomesticWater"]


class DomesticHotWater(Water):
    node_type: URIRef = s223["Water-DomesticHotWater"]


class ChilledWater(Water):
    node_type: URIRef = s223["Water-ChilledWater"]


class HotWater(Water):
    node_type: URIRef = s223["Water-HotWater"]


class CondensedWater(Water):
    node_type: URIRef = s223["Water-CondensedWater"]


class GlycoledWater(Water):
    # glycol_proportion =
    node_type: URIRef = s223["Water-GlycoledWater"]


class Steam(Water):
    # glycol_proportion =
    node_type: URIRef = s223["Water-Steam"]


# Connections

# A class factory that would build everything ?
# lst_of_substance_classes = [HotWater, ChilledWater, ... ]
# for each in lst_of_substance_classes:


# === WATER
class WaterConnection(Connection):
    hasMedium: URIRef = Water.node_type
    node_type = None


class WaterConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Water.node_type
    node_type = None


class WaterInletConnectionPoint(InletConnectionPoint, WaterConnectionPoint):
    node_type = None


class WaterOutletConnectionPoint(OutletConnectionPoint, WaterConnectionPoint):
    node_type = None


class WaterSystemConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Water.node_type
    node_type = None


class WaterInletSystemConnectionPoint(InletConnectionPoint, WaterConnectionPoint):
    node_type = None


class WaterOutletSystemConnectionPoint(OutletConnectionPoint, WaterConnectionPoint):
    node_type = None


# === HOT WATER
class HotWaterConnection(WaterConnection):
    hasMedium: URIRef = HotWater.node_type
    node_type = None


class HotWaterConnectionPoint(WaterConnectionPoint):
    hasMedium: URIRef = HotWater.node_type
    node_type = None


class HotWaterInletConnectionPoint(InletConnectionPoint, HotWaterConnectionPoint):
    node_type = None


class HotWaterOutletConnectionPoint(OutletConnectionPoint, HotWaterConnectionPoint):
    node_type = None


class HotWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: URIRef = HotWater.node_type
    node_type = None


class HotWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    node_type = None


class HotWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    node_type = None


# === STEAM
class SteamConnection(Connection):
    hasMedium: URIRef = Steam.node_type
    node_type = None


class SteamConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Steam.node_type
    node_type = None


class SteamInletConnectionPoint(InletConnectionPoint, SteamConnectionPoint):
    node_type = None


class SteamOutletConnectionPoint(OutletConnectionPoint, SteamConnectionPoint):
    node_type = None


class SteamSystemConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Steam.node_type
    node_type = None


class SteamInletSystemConnectionPoint(InletConnectionPoint, SteamSystemConnectionPoint):
    node_type = None


class SteamOutletSystemConnectionPoint(
    OutletConnectionPoint, SteamSystemConnectionPoint
):
    node_type = None


# === CHILLED WATER
class ChilledWaterConnection(WaterConnection):
    hasMedium: URIRef = ChilledWater.node_type
    node_type = None


class ChilledWaterConnectionPoint(WaterConnectionPoint):
    hasMedium: URIRef = ChilledWater.node_type
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
    hasMedium: URIRef = ChilledWater.node_type
    node_type = None


class ChilledWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    node_type = None


class ChilledWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    node_type = None


# === CONDENSED WATER
class CondensedWaterConnection(WaterConnection):
    hasMedium: URIRef = CondensedWater.node_type
    node_type = None


class CondensedWaterConnectionPoint(WaterConnectionPoint):
    hasMedium: URIRef = CondensedWater.node_type
    node_type = None


class CondensedWaterInletConnectionPoint(
    InletConnectionPoint, CondensedWaterConnectionPoint
):
    node_type = None


class CondensedWaterOutletConnectionPoint(
    OutletConnectionPoint, CondensedWaterConnectionPoint
):
    node_type = None


class CondensedWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: URIRef = CondensedWater.node_type
    node_type = None


class CondensedWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, CondensedWaterSystemConnectionPoint
):
    node_type = None


class CondensedWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, CondensedWaterSystemConnectionPoint
):
    node_type = None
