from rdflib import URIRef
from ..core import s223, enum

from ..node import (
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

__namespace__ = enum

# Medium
class Water(Medium):
    node_type: URIRef = enum.Medium_Water


class DomesticWater(Water):
    node_type: URIRef = enum.Water_DomesticWater


class DomesticHotWater(Water):
    node_type: URIRef = enum.Water_DomesticHotWater


class ChilledWater(Water):
    node_type: URIRef = enum.Water_ChilledWater


class HotWater(Water):
    node_type: URIRef = enum.Water_HotWater


class CondensedWater(Water):
    node_type: URIRef = enum.Water_CondensedWater


class GlycoledWater(Water):
    # glycol_proportion =
    node_type: URIRef = enum.Water_GlycoledWater


class Steam(Water):
    # glycol_proportion =
    node_type: URIRef = enum.Water_Steam


# Connections

# A class factory that would build everything ?
# lst_of_substance_classes = [HotWater, ChilledWater, ... ]
# for each in lst_of_substance_classes:


# === WATER
class WaterConnection(Connection):
    hasSubstance: URIRef = Water.node_type
    node_type = None


class WaterConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = Water.node_type
    node_type = None


class WaterInletConnectionPoint(InletConnectionPoint, WaterConnectionPoint):
    node_type = None


class WaterOutletConnectionPoint(OutletConnectionPoint, WaterConnectionPoint):
    node_type = None


class WaterSystemConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = Water.node_type
    node_type = None


class WaterInletSystemConnectionPoint(InletConnectionPoint, WaterConnectionPoint):
    node_type = None


class WaterOutletSystemConnectionPoint(OutletConnectionPoint, WaterConnectionPoint):
    node_type = None


# === HOT WATER
class HotWaterConnection(Connection):
    hasSubstance: URIRef = HotWater.node_type
    node_type = None


class HotWaterConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = HotWater.node_type
    node_type = None


class HotWaterInletConnectionPoint(InletConnectionPoint, HotWaterConnectionPoint):
    node_type = None


class HotWaterOutletConnectionPoint(OutletConnectionPoint, HotWaterConnectionPoint):
    node_type = None


class HotWaterSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance: URIRef = HotWater.node_type
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
class SteamConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = Steam.node_type
    node_type = None


class SteamInletConnectionPoint(InletConnectionPoint, SteamConnectionPoint):
    node_type = None


class SteamOutletConnectionPoint(OutletConnectionPoint, SteamConnectionPoint):
    node_type = None


class SteamSystemConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = Steam.node_type
    node_type = None


class SteamInletSystemConnectionPoint(InletConnectionPoint, SteamSystemConnectionPoint):
    node_type = None


class SteamOutletSystemConnectionPoint(
    OutletConnectionPoint, SteamSystemConnectionPoint
):
    node_type = None


# === CHILLED WATER
class ChilledWaterConnection(Connection):
    hasSubstance: URIRef = ChilledWater.node_type
    node_type = None


class ChilledWaterConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = ChilledWater.node_type
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
    hasSubstance: URIRef = ChilledWater.node_type
    node_type = None


class ChilledWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    node_type = None


class ChilledWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    node_type = None
