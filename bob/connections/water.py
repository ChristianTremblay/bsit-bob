from rdflib import URIRef
from ..core import s223, p223

from ..core import (
    Medium,
    Water,
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

DomesticWater = Medium(node_iri=s223["Water-DomesticWater"])
DomesticHotWater = Medium(node_iri=s223["Water-DomesticHotWater"])
ChilledWater = Medium(node_iri=s223["Water-ChilledWater"])
HotWater = Medium(node_iri=s223["Water-HotWater"])
CondensedWater = Medium(node_iri=s223["Water-CondensedWater"])
MixedWater = Medium(node_iri=s223["Water-MixedWater"])
GlycoledWater = Medium(node_iri=s223["Water-GlycoledWater"])
Steam = Medium(node_iri=s223["Water-Steam"])

# class DomesticWater(Water):
#     node_type: URIRef = s223["Water-DomesticWater"]


# class DomesticHotWater(Water):
#     node_type: URIRef = s223["Water-DomesticHotWater"]


# class ChilledWater(Water):
#     node_type: URIRef = s223["Water-ChilledWater"]


# class HotWater(Water):
#     node_type: URIRef = s223["Water-HotWater"]


# class CondensedWater(Water):
#     node_type: URIRef = s223["Water-CondensedWater"]


# class GlycoledWater(Water):
#     # glycol_proportion =
#     node_type: URIRef = s223["Water-GlycoledWater"]


# class Steam(Water):
#     # glycol_proportion =
#     node_type: URIRef = s223["Water-Steam"]


# Connections

# A class factory that would build everything ?
# lst_of_substance_classes = [HotWater, ChilledWater, ... ]
# for each in lst_of_substance_classes:


# === WATER
class WaterConnection(Connection):
    hasMedium: Medium = Water
    node_type = None


class WaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water
    node_type = None


class WaterInletConnectionPoint(InletConnectionPoint, WaterConnectionPoint):
    node_type = None


class WaterOutletConnectionPoint(OutletConnectionPoint, WaterConnectionPoint):
    node_type = None


class WaterSystemConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water
    node_type = None


class WaterInletSystemConnectionPoint(InletConnectionPoint, WaterConnectionPoint):
    node_type = None


class WaterOutletSystemConnectionPoint(OutletConnectionPoint, WaterConnectionPoint):
    node_type = None


# === HOT WATER
class HotWaterConnection(Connection):
    hasMedium: Medium = HotWater
    node_type = None


class HotWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = HotWater
    node_type = None


class HotWaterInletConnectionPoint(InletConnectionPoint, HotWaterConnectionPoint):
    node_type = None


class HotWaterOutletConnectionPoint(OutletConnectionPoint, HotWaterConnectionPoint):
    node_type = None


class HotWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = HotWater
    node_type = None


class HotWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    node_type = None


class HotWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    node_type = None


# === HOT WATER
class MixedWaterConnection(Connection):
    hasMedium: Medium = MixedWater
    node_type = None


class MixedWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = MixedWater
    node_type = None


class MixedWaterInletConnectionPoint(InletConnectionPoint, MixedWaterConnectionPoint):
    node_type = None


class MixedWaterOutletConnectionPoint(OutletConnectionPoint, MixedWaterConnectionPoint):
    node_type = None


class MixedWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = MixedWater
    node_type = None


class MixedWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, MixedWaterSystemConnectionPoint
):
    node_type = None


class MixedWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, MixedWaterSystemConnectionPoint
):
    node_type = None


# === STEAM
class SteamConnection(Connection):
    hasMedium: Medium = Steam
    node_type = None


class SteamConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Steam
    node_type = None


class SteamInletConnectionPoint(InletConnectionPoint, SteamConnectionPoint):
    node_type = None


class SteamOutletConnectionPoint(OutletConnectionPoint, SteamConnectionPoint):
    node_type = None


class SteamSystemConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Steam
    node_type = None


class SteamInletSystemConnectionPoint(InletConnectionPoint, SteamSystemConnectionPoint):
    node_type = None


class SteamOutletSystemConnectionPoint(
    OutletConnectionPoint, SteamSystemConnectionPoint
):
    node_type = None


# === CHILLED WATER
class ChilledWaterConnection(Connection):
    hasMedium: Medium = ChilledWater
    node_type = None


class ChilledWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = ChilledWater
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
    hasMedium: Medium = ChilledWater
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
class CondensedWaterConnection(Connection):
    hasMedium: Medium = CondensedWater
    node_type = None


class CondensedWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = CondensedWater
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
    hasMedium: Medium = CondensedWater
    node_type = None


class CondensedWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, CondensedWaterSystemConnectionPoint
):
    node_type = None


class CondensedWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, CondensedWaterSystemConnectionPoint
):
    node_type = None
