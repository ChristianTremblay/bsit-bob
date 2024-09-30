from ..core import (
    BOB,
    S223,
    BidirectionalConnectionPoint,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    Medium,
)
from ..enum import Fluid, GlycolSolution_15Percent, GlycolSolution_30Percent, Water

_namespace = BOB


# Connections


# === Generic Fluid
class FluidConnection(Connection):
    _volatile = ("hasMedium",)
    hasMedium: Fluid = Water
    _class_iri = S223.Connection


class FluidConnectionPoint(ConnectionPoint):
    _volatile = ("hasMedium",)
    hasMedium: Fluid = Water


class FluidInletConnectionPoint(FluidConnectionPoint, InletConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class FluidOutletConnectionPoint(FluidConnectionPoint, OutletConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class FluidBidirectionalConnectionPoint(
    FluidConnectionPoint, BidirectionalConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint


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


# === MIXED WATER


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


# === Glycol Solution 15%


class Glycol30PercentConnection(Connection):
    hasMedium: Medium = GlycolSolution_30Percent
    _class_iri = S223.Connection


class Glycol30PercentConnectionPoint(ConnectionPoint):
    hasMedium: Medium = GlycolSolution_30Percent


class Glycol30PercentInletConnectionPoint(
    InletConnectionPoint, Glycol15PercentConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Glycol30PercentOutletConnectionPoint(
    OutletConnectionPoint, Glycol15PercentConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint
