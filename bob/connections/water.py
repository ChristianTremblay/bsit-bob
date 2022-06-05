from rdflib import URIRef

from ..core import (
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    Medium,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    SystemConnectionPoint,
    Water,
    p223,
    s223,
)

_namespace = s223

DomesticWater = Water("DomesticWater")
DomesticHotWater = Water("DomesticHotWater")
ChilledWater = Water("ChilledWater")
HotWater = Water("HotWater")
CondensedWater = Water("CondensedWater")
MixedWater = Water("MixedWater")
GlycoledWater = Water("GlycoledWater")
Steam = Water("Steam")

# class DomesticWater(Water):
#     _class_iri: URIRef = s223["Water-DomesticWater"]


# class DomesticHotWater(Water):
#     _class_iri: URIRef = s223["Water-DomesticHotWater"]


# class ChilledWater(Water):
#     _class_iri: URIRef = s223["Water-ChilledWater"]


# class HotWater(Water):
#     _class_iri: URIRef = s223["Water-HotWater"]


# class CondensedWater(Water):
#     _class_iri: URIRef = s223["Water-CondensedWater"]


# class GlycoledWater(Water):
#     # glycol_proportion =
#     _class_iri: URIRef = s223["Water-GlycoledWater"]


# class Steam(Water):
#     # glycol_proportion =
#     _class_iri: URIRef = s223["Water-Steam"]


# Connections

# A class factory that would build everything ?
# lst_of_substance_classes = [HotWater, ChilledWater, ... ]
# for each in lst_of_substance_classes:


# === WATER
class WaterConnection(Connection):
    hasMedium: Medium = Water
    _class_iri =None


class WaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water
    _class_iri =None


class WaterInletConnectionPoint(InletConnectionPoint, WaterConnectionPoint):
    _class_iri =None


class WaterOutletConnectionPoint(OutletConnectionPoint, WaterConnectionPoint):
    _class_iri =None


class WaterSystemConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water
    _class_iri =None


class WaterInletSystemConnectionPoint(InletConnectionPoint, WaterConnectionPoint):
    _class_iri =None


class WaterOutletSystemConnectionPoint(OutletConnectionPoint, WaterConnectionPoint):
    _class_iri =None


# === HOT WATER
class HotWaterConnection(Connection):
    hasMedium: Medium = HotWater
    _class_iri =None


class HotWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = HotWater
    _class_iri =None


class HotWaterInletConnectionPoint(InletConnectionPoint, HotWaterConnectionPoint):
    _class_iri =None


class HotWaterOutletConnectionPoint(OutletConnectionPoint, HotWaterConnectionPoint):
    _class_iri =None


class HotWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = HotWater
    _class_iri =None


class HotWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    _class_iri =None


class HotWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    _class_iri =None


# === HOT WATER
class MixedWaterConnection(Connection):
    hasMedium: Medium = MixedWater
    _class_iri =None


class MixedWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = MixedWater
    _class_iri =None


class MixedWaterInletConnectionPoint(InletConnectionPoint, MixedWaterConnectionPoint):
    _class_iri =None


class MixedWaterOutletConnectionPoint(OutletConnectionPoint, MixedWaterConnectionPoint):
    _class_iri =None


class MixedWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = MixedWater
    _class_iri =None


class MixedWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, MixedWaterSystemConnectionPoint
):
    _class_iri =None


class MixedWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, MixedWaterSystemConnectionPoint
):
    _class_iri =None


# === STEAM
class SteamConnection(Connection):
    hasMedium: Medium = Steam
    _class_iri =None


class SteamConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Steam
    _class_iri =None


class SteamInletConnectionPoint(InletConnectionPoint, SteamConnectionPoint):
    _class_iri =None


class SteamOutletConnectionPoint(OutletConnectionPoint, SteamConnectionPoint):
    _class_iri =None


class SteamSystemConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Steam
    _class_iri =None


class SteamInletSystemConnectionPoint(InletConnectionPoint, SteamSystemConnectionPoint):
    _class_iri =None


class SteamOutletSystemConnectionPoint(
    OutletConnectionPoint, SteamSystemConnectionPoint
):
    _class_iri =None


# === CHILLED WATER
class ChilledWaterConnection(Connection):
    hasMedium: Medium = ChilledWater
    _class_iri =None


class ChilledWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = ChilledWater
    _class_iri =None


class ChilledWaterInletConnectionPoint(
    InletConnectionPoint, ChilledWaterConnectionPoint
):
    _class_iri =None


class ChilledWaterOutletConnectionPoint(
    OutletConnectionPoint, ChilledWaterConnectionPoint
):
    _class_iri =None


class ChilledWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = ChilledWater
    _class_iri =None


class ChilledWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    _class_iri =None


class ChilledWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    _class_iri =None


# === CONDENSED WATER
class CondensedWaterConnection(Connection):
    hasMedium: Medium = CondensedWater
    _class_iri =None


class CondensedWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = CondensedWater
    _class_iri =None


class CondensedWaterInletConnectionPoint(
    InletConnectionPoint, CondensedWaterConnectionPoint
):
    _class_iri =None


class CondensedWaterOutletConnectionPoint(
    OutletConnectionPoint, CondensedWaterConnectionPoint
):
    _class_iri =None


class CondensedWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = CondensedWater
    _class_iri =None


class CondensedWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, CondensedWaterSystemConnectionPoint
):
    _class_iri =None


class CondensedWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, CondensedWaterSystemConnectionPoint
):
    _class_iri =None
