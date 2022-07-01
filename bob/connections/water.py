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
    BOB,
    P223,
    S223,
)

_namespace = BOB


# class DomesticWater(Water):
#     _class_iri: URIRef = S223["Water-DomesticWater"]


# class DomesticHotWater(Water):
#     _class_iri: URIRef = S223["Water-DomesticHotWater"]


# class ChilledWater(Water):
#     _class_iri: URIRef = S223["Water-ChilledWater"]


# class HotWater(Water):
#     _class_iri: URIRef = S223["Water-HotWater"]


# class CondensedWater(Water):
#     _class_iri: URIRef = S223["Water-CondensedWater"]


# class GlycoledWater(Water):
#     # glycol_proportion =
#     _class_iri: URIRef = S223["Water-GlycoledWater"]


# class Steam(Water):
#     # glycol_proportion =
#     _class_iri: URIRef = S223["Water-Steam"]


# Connections

# A class factory that would build everything ?
# lst_of_substance_classes = [HotWater, ChilledWater, ... ]
# for each in lst_of_substance_classes:


# === WATER
class WaterConnection(Connection):
    hasMedium: Medium = Water
    _class_iri = S223.Connection


class WaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water


class WaterInletConnectionPoint(InletConnectionPoint, WaterConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class WaterOutletConnectionPoint(OutletConnectionPoint, WaterConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class WaterSystemConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water


class WaterInletSystemConnectionPoint(InletConnectionPoint, WaterConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class WaterOutletSystemConnectionPoint(OutletConnectionPoint, WaterConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


# === HOT WATER
class HotWaterConnection(Connection):
    hasMedium: Medium = Water.HotWater
    _class_iri = S223.Connection


class HotWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water.HotWater


class HotWaterInletConnectionPoint(InletConnectionPoint, HotWaterConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class HotWaterOutletConnectionPoint(OutletConnectionPoint, HotWaterConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class HotWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Water.HotWater


class HotWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class HotWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === HOT WATER
class MixedWaterConnection(Connection):
    hasMedium: Medium = Water.MixedWater
    _class_iri = S223.Connection


class MixedWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water.MixedWater


class MixedWaterInletConnectionPoint(InletConnectionPoint, MixedWaterConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class MixedWaterOutletConnectionPoint(OutletConnectionPoint, MixedWaterConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class MixedWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Water.MixedWater


class MixedWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, MixedWaterSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class MixedWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, MixedWaterSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === STEAM
class SteamConnection(Connection):
    hasMedium: Medium = Water.Steam
    _class_iri = S223.Connection


class SteamConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water.Steam


class SteamInletConnectionPoint(InletConnectionPoint, SteamConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class SteamOutletConnectionPoint(OutletConnectionPoint, SteamConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class SteamSystemConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water.Steam


class SteamInletSystemConnectionPoint(InletConnectionPoint, SteamSystemConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class SteamOutletSystemConnectionPoint(
    OutletConnectionPoint, SteamSystemConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


# === CHILLED WATER
class ChilledWaterConnection(Connection):
    hasMedium: Medium = Water.ChilledWater
    _class_iri = S223.Connection


class ChilledWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water.ChilledWater


class ChilledWaterInletConnectionPoint(
    InletConnectionPoint, ChilledWaterConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class ChilledWaterOutletConnectionPoint(
    OutletConnectionPoint, ChilledWaterConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class ChilledWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Water.ChilledWater


class ChilledWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class ChilledWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === CONDENSED WATER
class CondensedWaterConnection(Connection):
    hasMedium: Medium = Water.CondensedWater
    _class_iri = S223.Connection


class CondensedWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water.CondensedWater


class CondensedWaterInletConnectionPoint(
    InletConnectionPoint, CondensedWaterConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class CondensedWaterOutletConnectionPoint(
    OutletConnectionPoint, CondensedWaterConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class CondensedWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Water.CondensedWater


class CondensedWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, CondensedWaterSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class CondensedWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, CondensedWaterSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint
