from rdflib import URIRef

from ..core import (
    BOB,
    P223,
    S223,
    BidirectionalConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    Medium,
)
from ..enum import GlycolSolution_15Percent, GlycolSolution_30Percent, Water

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


class WaterInletConnectionPoint(WaterConnectionPoint, InletConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class WaterOutletConnectionPoint(WaterConnectionPoint, OutletConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class WaterBidirectionalConnectionPoint(
    WaterConnectionPoint, BidirectionalConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint


# === HOT WATER


class HotWaterConnection(Connection):
    hasMedium: Medium = Water.HotWater
    _class_iri = S223.Connection


class HotWaterConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Water.HotWater


class HotWaterInletConnectionPoint(HotWaterConnectionPoint, InletConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class HotWaterOutletConnectionPoint(HotWaterConnectionPoint, OutletConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


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


# === Glycol Solution 15%


class Glycol15PercentConnection(Connection):
    hasMedium: Medium = GlycolSolution_15Percent
    _class_iri = S223.Connection


class Glycol15PercentConnectionPoint(ConnectionPoint):
    hasMedium: Medium = GlycolSolution_15Percent


class Glycol15PercentInletConnectionPoint(
    InletConnectionPoint, Glycol15PercentConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Glycol15PercentOutletConnectionPoint(
    OutletConnectionPoint, Glycol15PercentConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint
