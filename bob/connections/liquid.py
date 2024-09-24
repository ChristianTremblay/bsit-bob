from rdflib import URIRef

from ..core import (
    BOB,
    P223,
    S223,
    BidirectionalConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    Medium,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    SystemConnectionPoint,
)
from ..enum import Fluid, GlycolSolution_15Percent, GlycolSolution_30Percent, Water

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


# === Generic Fluid
class FluidConnection(Connection):
    _volatile = ("hasMedium",)
    hasMedium: Fluid = Water
    _class_iri = S223.Connection

    def __inif__(self, hasMedium=Water, **kwargs):
        super().__init__(hasMedium=hasMedium, **kwargs)


class FluidConnectionPoint(ConnectionPoint):
    _volatile = ("hasMedium",)
    hasMedium: Fluid = Water

    def __inif__(self, hasMedium=Water, **kwargs):
        super().__init__(hasMedium=hasMedium, **kwargs)


class FluidInletConnectionPoint(FluidConnectionPoint, InletConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class FluidOutletConnectionPoint(FluidConnectionPoint, OutletConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class FluidBidirectionalConnectionPoint(
    FluidConnectionPoint, BidirectionalConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint


class FluidSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Fluid = Water


class FluidInletSystemConnectionPoint(
    FluidSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class FLuidOutletSystemConnectionPoint(
    FluidSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === WATER
class WaterConnection(Connection):
    _volatile = ("hasMedium",)
    hasMedium: Medium = Water
    _class_iri = S223.Connection


class WaterConnectionPoint(ConnectionPoint):
    _volatile = ("hasMedium",)
    hasMedium: Medium = Water


class WaterInletConnectionPoint(WaterConnectionPoint, InletConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class WaterOutletConnectionPoint(WaterConnectionPoint, OutletConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class WaterBidirectionalConnectionPoint(
    WaterConnectionPoint, BidirectionalConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint


class WaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Water


class WaterInletSystemConnectionPoint(
    WaterSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class WaterOutletSystemConnectionPoint(
    WaterSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


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


class HotWaterSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Water.HotWater


class HotWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class HotWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


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
    _class_iri = BOB.InletSystemConnectionPoint


class MixedWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, MixedWaterSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


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


class SteamSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Water.Steam


class SteamInletSystemConnectionPoint(
    InletSystemConnectionPoint, SteamSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class SteamOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, SteamSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


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
    _class_iri = BOB.InletSystemConnectionPoint


class ChilledWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


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
    _class_iri = BOB.InletSystemConnectionPoint


class CondensedWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, CondensedWaterSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


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


class Glycol15PercentSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = GlycolSolution_15Percent


class Glycol15PercentInletSystemConnectionPoint(
    InletSystemConnectionPoint, Glycol15PercentSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Glycol15PercentOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, Glycol15PercentSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint
