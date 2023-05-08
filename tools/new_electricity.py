from rdflib import Literal, URIRef

from ..core import (
    BOB,
    S223,
    Connection,
    ConnectionPoint,
    Electricity,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    SystemConnectionPoint,
)

_namespace = S223

# === Generic
# Undefined Electrical


class ElectricalConnection(Connection):
    hasMedium = Electricity
    _class_iri = S223.Connection


class ElectricalConnectionPoint(ConnectionPoint):
    hasMedium = Electricity


class ElectricalInletConnectionPoint(InletConnectionPoint, ElectricalConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class ElectricalOutletConnectionPoint(OutletConnectionPoint, ElectricalConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class ElectricalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity


class ElectricalSystemInletConnectionPoint(
    ElectricalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class ElectricalSystemOutletConnectionPoint(
    ElectricalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-1.73kV-1Ph-60Hz
# 1 phase


class Electricity_1r73kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC1r73kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_1r73kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC1r73kV_1Ph_60Hz


class Electricity_1r73kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_1r73kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_1r73kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_1r73kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_1r73kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC1r73kV_1Ph_60Hz


class Electricity_1r73kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_1r73kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_1r73kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_1r73kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-1.91kV-1Ph-60Hz
# 1 phase


class Electricity_1r91kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC1r91kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_1r91kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC1r91kV_1Ph_60Hz


class Electricity_1r91kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_1r91kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_1r91kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_1r91kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_1r91kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC1r91kV_1Ph_60Hz


class Electricity_1r91kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_1r91kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_1r91kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_1r91kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-10.0kV-3Ph-60Hz
# 3 Phases


class Electricity_10r0kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC10r0kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_10r0kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC10r0kV_3Ph_60Hz


class Electricity_10r0kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_10r0kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_10r0kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_10r0kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_10r0kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC10r0kV_3Ph_60Hz


class Electricity_10r0kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_10r0kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_10r0kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_10r0kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-10.0kV-5.77kV-1Ph-60Hz
# 1 phase


class Electricity_10r0kV_5r77kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC10r0kV_5r77kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_10r0kV_5r77kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC10r0kV_5r77kV_1Ph_60Hz


class Electricity_10r0kV_5r77kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_10r0kV_5r77kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_10r0kV_5r77kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_10r0kV_5r77kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_10r0kV_5r77kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC10r0kV_5r77kV_1Ph_60Hz


class Electricity_10r0kV_5r77kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_10r0kV_5r77kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_10r0kV_5r77kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_10r0kV_5r77kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-10.0kV-5.77kV-3Ph-60Hz
# 3 Phases


class Electricity_10r0kV_5r77kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC10r0kV_5r77kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_10r0kV_5r77kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC10r0kV_5r77kV_3Ph_60Hz


class Electricity_10r0kV_5r77kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_10r0kV_5r77kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_10r0kV_5r77kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_10r0kV_5r77kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_10r0kV_5r77kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC10r0kV_5r77kV_3Ph_60Hz


class Electricity_10r0kV_5r77kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_10r0kV_5r77kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_10r0kV_5r77kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_10r0kV_5r77kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-110V-1Ph-50Hz
# 1 phase


class Electricity_110V_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC110V_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_110V_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC110V_1Ph_50Hz


class Electricity_110V_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_110V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_110V_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_110V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_110V_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC110V_1Ph_50Hz


class Electricity_110V_1Ph_50HzSystemInletConnectionPoint(
    Electricity_110V_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_110V_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_110V_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-120V-1Ph-60Hz
# 1 phase


class Electricity_120V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC120V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_120V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC120V_1Ph_60Hz


class Electricity_120V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_120V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_120V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_120V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_120V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC120V_1Ph_60Hz


class Electricity_120V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_120V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_120V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_120V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-127V-1Ph-50Hz
# 1 phase


class Electricity_127V_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC127V_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_127V_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC127V_1Ph_50Hz


class Electricity_127V_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_127V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_127V_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_127V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_127V_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC127V_1Ph_50Hz


class Electricity_127V_1Ph_50HzSystemInletConnectionPoint(
    Electricity_127V_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_127V_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_127V_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-139V-1Ph-50Hz
# 1 phase


class Electricity_139V_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC139V_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_139V_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC139V_1Ph_50Hz


class Electricity_139V_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_139V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_139V_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_139V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_139V_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC139V_1Ph_50Hz


class Electricity_139V_1Ph_50HzSystemInletConnectionPoint(
    Electricity_139V_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_139V_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_139V_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-190V-110V-1Ph-50Hz
# 1 phase


class Electricity_190V_110V_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC190V_110V_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_190V_110V_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC190V_110V_1Ph_50Hz


class Electricity_190V_110V_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_190V_110V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_190V_110V_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_190V_110V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_190V_110V_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC190V_110V_1Ph_50Hz


class Electricity_190V_110V_1Ph_50HzSystemInletConnectionPoint(
    Electricity_190V_110V_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_190V_110V_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_190V_110V_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-190V-110V-3Ph-50Hz
# 3 Phases


class Electricity_190V_110V_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC190V_110V_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_190V_110V_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC190V_110V_3Ph_50Hz


class Electricity_190V_110V_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_190V_110V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_190V_110V_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_190V_110V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_190V_110V_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC190V_110V_3Ph_50Hz


class Electricity_190V_110V_3Ph_50HzSystemInletConnectionPoint(
    Electricity_190V_110V_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_190V_110V_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_190V_110V_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-190V-3Ph-50Hz
# 3 Phases


class Electricity_190V_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC190V_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_190V_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC190V_3Ph_50Hz


class Electricity_190V_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_190V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_190V_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_190V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_190V_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC190V_3Ph_50Hz


class Electricity_190V_3Ph_50HzSystemInletConnectionPoint(
    Electricity_190V_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_190V_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_190V_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-2.4kV-1Ph-60Hz
# 1 phase


class Electricity_2r4kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC2r4kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_2r4kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC2r4kV_1Ph_60Hz


class Electricity_2r4kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_2r4kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_2r4kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_2r4kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_2r4kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC2r4kV_1Ph_60Hz


class Electricity_2r4kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_2r4kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_2r4kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_2r4kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-208V-120V-1Ph-60Hz
# 1 phase


class Electricity_208V_120V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC208V_120V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_208V_120V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC208V_120V_1Ph_60Hz


class Electricity_208V_120V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208V_120V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_208V_120V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208V_120V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_208V_120V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC208V_120V_1Ph_60Hz


class Electricity_208V_120V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_208V_120V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_208V_120V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_208V_120V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-208V-120V-3Ph-60Hz
# 3 Phases


class Electricity_208V_120V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC208V_120V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_208V_120V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC208V_120V_3Ph_60Hz


class Electricity_208V_120V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208V_120V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_208V_120V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208V_120V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_208V_120V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC208V_120V_3Ph_60Hz


class Electricity_208V_120V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_208V_120V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_208V_120V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_208V_120V_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-208V-1Ph-60Hz
# 1 phase


class Electricity_208V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC208V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_208V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC208V_1Ph_60Hz


class Electricity_208V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_208V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_208V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC208V_1Ph_60Hz


class Electricity_208V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_208V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_208V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_208V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-208V-3Ph-60Hz
# 3 Phases


class Electricity_208V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC208V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_208V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC208V_3Ph_60Hz


class Electricity_208V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_208V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_208V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC208V_3Ph_60Hz


class Electricity_208V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_208V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_208V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_208V_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-219V-1Ph-60Hz
# 1 phase


class Electricity_219V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC219V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_219V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC219V_1Ph_60Hz


class Electricity_219V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_219V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_219V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_219V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_219V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC219V_1Ph_60Hz


class Electricity_219V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_219V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_219V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_219V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-220V-127V-1Ph-50Hz
# 1 phase


class Electricity_220V_127V_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC220V_127V_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_220V_127V_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC220V_127V_1Ph_50Hz


class Electricity_220V_127V_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_220V_127V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_220V_127V_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_220V_127V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_220V_127V_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC220V_127V_1Ph_50Hz


class Electricity_220V_127V_1Ph_50HzSystemInletConnectionPoint(
    Electricity_220V_127V_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_220V_127V_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_220V_127V_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-220V-127V-3Ph-50Hz
# 3 Phases


class Electricity_220V_127V_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC220V_127V_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_220V_127V_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC220V_127V_3Ph_50Hz


class Electricity_220V_127V_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_220V_127V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_220V_127V_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_220V_127V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_220V_127V_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC220V_127V_3Ph_50Hz


class Electricity_220V_127V_3Ph_50HzSystemInletConnectionPoint(
    Electricity_220V_127V_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_220V_127V_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_220V_127V_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-220V-3Ph-50Hz
# 3 Phases


class Electricity_220V_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC220V_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_220V_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC220V_3Ph_50Hz


class Electricity_220V_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_220V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_220V_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_220V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_220V_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC220V_3Ph_50Hz


class Electricity_220V_3Ph_50HzSystemInletConnectionPoint(
    Electricity_220V_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_220V_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_220V_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-231V-1Ph-50Hz
# 1 phase


class Electricity_231V_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC231V_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_231V_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC231V_1Ph_50Hz


class Electricity_231V_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_231V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_231V_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_231V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_231V_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC231V_1Ph_50Hz


class Electricity_231V_1Ph_50HzSystemInletConnectionPoint(
    Electricity_231V_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_231V_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_231V_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240V-120V_1Ph-60Hz
# 1 phase


class Electricity_240V_120V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240V_120V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240V_120V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_120V_1Ph_60Hz


class Electricity_240V_120V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_120V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_120V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_120V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_120V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_120V_1Ph_60Hz


class Electricity_240V_120V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_240V_120V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240V_120V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_240V_120V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240V-139V-1Ph-50Hz
# 1 phase


class Electricity_240V_139V_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC240V_139V_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_240V_139V_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_139V_1Ph_50Hz


class Electricity_240V_139V_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_139V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_139V_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_139V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_139V_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_139V_1Ph_50Hz


class Electricity_240V_139V_1Ph_50HzSystemInletConnectionPoint(
    Electricity_240V_139V_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240V_139V_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_240V_139V_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240V-139V-3Ph-50Hz
# 3 Phases


class Electricity_240V_139V_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC240V_139V_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_240V_139V_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_139V_3Ph_50Hz


class Electricity_240V_139V_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_139V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_139V_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_139V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_139V_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_139V_3Ph_50Hz


class Electricity_240V_139V_3Ph_50HzSystemInletConnectionPoint(
    Electricity_240V_139V_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240V_139V_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_240V_139V_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240V-1Ph-50Hz
# 1 phase


class Electricity_240V_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC240V_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_240V_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_1Ph_50Hz


class Electricity_240V_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_1Ph_50Hz


class Electricity_240V_1Ph_50HzSystemInletConnectionPoint(
    Electricity_240V_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240V_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_240V_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240V-1Ph-60Hz
# 1 phase


class Electricity_240V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_1Ph_60Hz


class Electricity_240V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_1Ph_60Hz


class Electricity_240V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_240V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_240V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240V-208V-120V-3Ph-60Hz
# 3 Phases


class Electricity_240V_208V_120V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240V_208V_120V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240V_208V_120V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_208V_120V_3Ph_60Hz


class Electricity_240V_208V_120V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_208V_120V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_208V_120V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_208V_120V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_208V_120V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_208V_120V_3Ph_60Hz


class Electricity_240V_208V_120V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_240V_208V_120V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240V_208V_120V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_240V_208V_120V_3Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240V-208V-1Ph-60Hz
# 1 phase


class Electricity_240V_208V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240V_208V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240V_208V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_208V_1Ph_60Hz


class Electricity_240V_208V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_208V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_208V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_208V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_208V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_208V_1Ph_60Hz


class Electricity_240V_208V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_240V_208V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240V_208V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_240V_208V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240V-208V-3Ph-60Hz
# 3 Phases


class Electricity_240V_208V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240V_208V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240V_208V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_208V_3Ph_60Hz


class Electricity_240V_208V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_208V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_208V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_208V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_208V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_208V_3Ph_60Hz


class Electricity_240V_208V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_240V_208V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240V_208V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_240V_208V_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240V-3Ph-50Hz
# 3 Phases


class Electricity_240V_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC240V_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_240V_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_3Ph_50Hz


class Electricity_240V_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_3Ph_50Hz


class Electricity_240V_3Ph_50HzSystemInletConnectionPoint(
    Electricity_240V_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240V_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_240V_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240V-3Ph-60Hz
# 3 Phases


class Electricity_240V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_3Ph_60Hz


class Electricity_240V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_3Ph_60Hz


class Electricity_240V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_240V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_240V_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-24V-1Ph-60Hz
# 1 phase


class Electricity_24V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC24V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_24V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC24V_1Ph_60Hz


class Electricity_24V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_24V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_24V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_24V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_24V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC24V_1Ph_60Hz


class Electricity_24V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_24V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_24V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_24V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-277V-1Ph-60Hz
# 1 phase


class Electricity_277V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC277V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_277V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC277V_1Ph_60Hz


class Electricity_277V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_277V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_277V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_277V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_277V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC277V_1Ph_60Hz


class Electricity_277V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_277V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_277V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_277V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3.0kV-1.73kV-1Ph-60Hz
# 1 phase


class Electricity_3r0kV_1r73kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3r0kV_1r73kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3r0kV_1r73kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3r0kV_1r73kV_1Ph_60Hz


class Electricity_3r0kV_1r73kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3r0kV_1r73kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3r0kV_1r73kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3r0kV_1r73kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3r0kV_1r73kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3r0kV_1r73kV_1Ph_60Hz


class Electricity_3r0kV_1r73kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_3r0kV_1r73kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3r0kV_1r73kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_3r0kV_1r73kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3.0kV-1.73kV-3Ph-60Hz
# 3 Phases


class Electricity_3r0kV_1r73kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3r0kV_1r73kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3r0kV_1r73kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3r0kV_1r73kV_3Ph_60Hz


class Electricity_3r0kV_1r73kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3r0kV_1r73kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3r0kV_1r73kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3r0kV_1r73kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3r0kV_1r73kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3r0kV_1r73kV_3Ph_60Hz


class Electricity_3r0kV_1r73kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_3r0kV_1r73kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3r0kV_1r73kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_3r0kV_1r73kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3.0kV-3Ph-60Hz
# 3 Phases


class Electricity_3r0kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3r0kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3r0kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3r0kV_3Ph_60Hz


class Electricity_3r0kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3r0kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3r0kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3r0kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3r0kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3r0kV_3Ph_60Hz


class Electricity_3r0kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_3r0kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3r0kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_3r0kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3.3kV-1.91kV-1Ph-60Hz
# 1 phase


class Electricity_3r3kV_1r91kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3r3kV_1r91kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3r3kV_1r91kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3r3kV_1r91kV_1Ph_60Hz


class Electricity_3r3kV_1r91kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3r3kV_1r91kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3r3kV_1r91kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3r3kV_1r91kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3r3kV_1r91kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3r3kV_1r91kV_1Ph_60Hz


class Electricity_3r3kV_1r91kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_3r3kV_1r91kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3r3kV_1r91kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_3r3kV_1r91kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3.3kV-1.91kV-3Ph-60Hz
# 3 Phases


class Electricity_3r3kV_1r91kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3r3kV_1r91kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3r3kV_1r91kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3r3kV_1r91kV_3Ph_60Hz


class Electricity_3r3kV_1r91kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3r3kV_1r91kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3r3kV_1r91kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3r3kV_1r91kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3r3kV_1r91kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3r3kV_1r91kV_3Ph_60Hz


class Electricity_3r3kV_1r91kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_3r3kV_1r91kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3r3kV_1r91kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_3r3kV_1r91kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3.3kV-3Ph-60Hz
# 3 Phases


class Electricity_3r3kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3r3kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3r3kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3r3kV_3Ph_60Hz


class Electricity_3r3kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3r3kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3r3kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3r3kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3r3kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3r3kV_3Ph_60Hz


class Electricity_3r3kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_3r3kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3r3kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_3r3kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3.46kV-1Ph-60Hz
# 1 phase


class Electricity_3r46kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3r46kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3r46kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3r46kV_1Ph_60Hz


class Electricity_3r46kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3r46kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3r46kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3r46kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3r46kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3r46kV_1Ph_60Hz


class Electricity_3r46kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_3r46kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3r46kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_3r46kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3.81kV-1Ph-60Hz
# 1 phase


class Electricity_3r81kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3r81kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3r81kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3r81kV_1Ph_60Hz


class Electricity_3r81kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3r81kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3r81kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3r81kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3r81kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3r81kV_1Ph_60Hz


class Electricity_3r81kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_3r81kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3r81kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_3r81kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-347V-1Ph-60Hz
# 1 phase


class Electricity_347V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC347V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_347V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC347V_1Ph_60Hz


class Electricity_347V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_347V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_347V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_347V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_347V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC347V_1Ph_60Hz


class Electricity_347V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_347V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_347V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_347V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-380V-219V-1Ph-60Hz
# 1 phase


class Electricity_380V_219V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC380V_219V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_380V_219V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC380V_219V_1Ph_60Hz


class Electricity_380V_219V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_380V_219V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_380V_219V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_380V_219V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_380V_219V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC380V_219V_1Ph_60Hz


class Electricity_380V_219V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_380V_219V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_380V_219V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_380V_219V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-380V-219V-3Ph-60Hz
# 3 Phases


class Electricity_380V_219V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC380V_219V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_380V_219V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC380V_219V_3Ph_60Hz


class Electricity_380V_219V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_380V_219V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_380V_219V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_380V_219V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_380V_219V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC380V_219V_3Ph_60Hz


class Electricity_380V_219V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_380V_219V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_380V_219V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_380V_219V_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-380V-3Ph-60Hz
# 3 Phases


class Electricity_380V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC380V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_380V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC380V_3Ph_60Hz


class Electricity_380V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_380V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_380V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_380V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_380V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC380V_3Ph_60Hz


class Electricity_380V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_380V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_380V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_380V_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-4.16kV-2.4kV-1Ph-60Hz
# 1 phase


class Electricity_4r16kV_2r4kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC4r16kV_2r4kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_4r16kV_2r4kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC4r16kV_2r4kV_1Ph_60Hz


class Electricity_4r16kV_2r4kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_4r16kV_2r4kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_4r16kV_2r4kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_4r16kV_2r4kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_4r16kV_2r4kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC4r16kV_2r4kV_1Ph_60Hz


class Electricity_4r16kV_2r4kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_4r16kV_2r4kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_4r16kV_2r4kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_4r16kV_2r4kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-4.16kV-2.4kV-3Ph-60Hz
# 3 Phases


class Electricity_4r16kV_2r4kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC4r16kV_2r4kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_4r16kV_2r4kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC4r16kV_2r4kV_3Ph_60Hz


class Electricity_4r16kV_2r4kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_4r16kV_2r4kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_4r16kV_2r4kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_4r16kV_2r4kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_4r16kV_2r4kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC4r16kV_2r4kV_3Ph_60Hz


class Electricity_4r16kV_2r4kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_4r16kV_2r4kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_4r16kV_2r4kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_4r16kV_2r4kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-4.16kV-3Ph-60Hz
# 3 Phases


class Electricity_4r16kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC4r16kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_4r16kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC4r16kV_3Ph_60Hz


class Electricity_4r16kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_4r16kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_4r16kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_4r16kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_4r16kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC4r16kV_3Ph_60Hz


class Electricity_4r16kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_4r16kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_4r16kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_4r16kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-400V-231V-1Ph-50Hz
# 1 phase


class Electricity_400V_231V_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC400V_231V_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_400V_231V_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC400V_231V_1Ph_50Hz


class Electricity_400V_231V_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_400V_231V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_400V_231V_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_400V_231V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_400V_231V_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC400V_231V_1Ph_50Hz


class Electricity_400V_231V_1Ph_50HzSystemInletConnectionPoint(
    Electricity_400V_231V_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_400V_231V_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_400V_231V_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-400V-231V-3Ph-50Hz
# 3 Phases


class Electricity_400V_231V_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC400V_231V_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_400V_231V_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC400V_231V_3Ph_50Hz


class Electricity_400V_231V_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_400V_231V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_400V_231V_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_400V_231V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_400V_231V_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC400V_231V_3Ph_50Hz


class Electricity_400V_231V_3Ph_50HzSystemInletConnectionPoint(
    Electricity_400V_231V_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_400V_231V_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_400V_231V_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-400V-3Ph-50Hz
# 3 Phases


class Electricity_400V_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC400V_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_400V_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC400V_3Ph_50Hz


class Electricity_400V_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_400V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_400V_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_400V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_400V_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC400V_3Ph_50Hz


class Electricity_400V_3Ph_50HzSystemInletConnectionPoint(
    Electricity_400V_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_400V_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_400V_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-415V-240V-1Ph-50Hz
# 1 phase


class Electricity_415V_240V_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC415V_240V_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_415V_240V_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC415V_240V_1Ph_50Hz


class Electricity_415V_240V_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_415V_240V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_415V_240V_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_415V_240V_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_415V_240V_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC415V_240V_1Ph_50Hz


class Electricity_415V_240V_1Ph_50HzSystemInletConnectionPoint(
    Electricity_415V_240V_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_415V_240V_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_415V_240V_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-415V-240V-3Ph-50Hz
# 3 Phases


class Electricity_415V_240V_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC415V_240V_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_415V_240V_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC415V_240V_3Ph_50Hz


class Electricity_415V_240V_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_415V_240V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_415V_240V_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_415V_240V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_415V_240V_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC415V_240V_3Ph_50Hz


class Electricity_415V_240V_3Ph_50HzSystemInletConnectionPoint(
    Electricity_415V_240V_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_415V_240V_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_415V_240V_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-415V-3Ph-50Hz
# 3 Phases


class Electricity_415V_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC415V_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_415V_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC415V_3Ph_50Hz


class Electricity_415V_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_415V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_415V_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_415V_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_415V_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC415V_3Ph_50Hz


class Electricity_415V_3Ph_50HzSystemInletConnectionPoint(
    Electricity_415V_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_415V_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_415V_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-480V-1Ph-60Hz
# 1 phase


class Electricity_480V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC480V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_480V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC480V_1Ph_60Hz


class Electricity_480V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_480V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_480V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC480V_1Ph_60Hz


class Electricity_480V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_480V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_480V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_480V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-480V-277V-1Ph-60Hz
# 1 phase


class Electricity_480V_277V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC480V_277V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_480V_277V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC480V_277V_1Ph_60Hz


class Electricity_480V_277V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480V_277V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_480V_277V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480V_277V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_480V_277V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC480V_277V_1Ph_60Hz


class Electricity_480V_277V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_480V_277V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_480V_277V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_480V_277V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-480V-277V-3Ph-60Hz
# 3 Phases


class Electricity_480V_277V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC480V_277V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_480V_277V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC480V_277V_3Ph_60Hz


class Electricity_480V_277V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480V_277V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_480V_277V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480V_277V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_480V_277V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC480V_277V_3Ph_60Hz


class Electricity_480V_277V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_480V_277V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_480V_277V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_480V_277V_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-480V-3Ph-60Hz
# 3 Phases


class Electricity_480V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC480V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_480V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC480V_3Ph_60Hz


class Electricity_480V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_480V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_480V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC480V_3Ph_60Hz


class Electricity_480V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_480V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_480V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_480V_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-5.77kV-1Ph-60Hz
# 1 phase


class Electricity_5r77kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC5r77kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_5r77kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC5r77kV_1Ph_60Hz


class Electricity_5r77kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_5r77kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_5r77kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_5r77kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_5r77kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC5r77kV_1Ph_60Hz


class Electricity_5r77kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_5r77kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_5r77kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_5r77kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6.0kV-3.46kV-1Ph-60Hz
# 1 phase


class Electricity_6r0kV_3r46kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6r0kV_3r46kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6r0kV_3r46kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6r0kV_3r46kV_1Ph_60Hz


class Electricity_6r0kV_3r46kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6r0kV_3r46kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6r0kV_3r46kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6r0kV_3r46kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6r0kV_3r46kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6r0kV_3r46kV_1Ph_60Hz


class Electricity_6r0kV_3r46kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_6r0kV_3r46kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6r0kV_3r46kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_6r0kV_3r46kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6.0kV-3.46kV-3Ph-60Hz
# 3 Phases


class Electricity_6r0kV_3r46kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6r0kV_3r46kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6r0kV_3r46kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6r0kV_3r46kV_3Ph_60Hz


class Electricity_6r0kV_3r46kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6r0kV_3r46kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6r0kV_3r46kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6r0kV_3r46kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6r0kV_3r46kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6r0kV_3r46kV_3Ph_60Hz


class Electricity_6r0kV_3r46kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_6r0kV_3r46kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6r0kV_3r46kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_6r0kV_3r46kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6.0kV-3Ph-60Hz
# 3 Phases


class Electricity_6r0kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6r0kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6r0kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6r0kV_3Ph_60Hz


class Electricity_6r0kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6r0kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6r0kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6r0kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6r0kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6r0kV_3Ph_60Hz


class Electricity_6r0kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_6r0kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6r0kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_6r0kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6.6kV-3.81kV-1Ph-60Hz
# 1 phase


class Electricity_6r6kV_3r81kV_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6r6kV_3r81kV_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6r6kV_3r81kV_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6r6kV_3r81kV_1Ph_60Hz


class Electricity_6r6kV_3r81kV_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6r6kV_3r81kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6r6kV_3r81kV_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6r6kV_3r81kV_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6r6kV_3r81kV_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6r6kV_3r81kV_1Ph_60Hz


class Electricity_6r6kV_3r81kV_1Ph_60HzSystemInletConnectionPoint(
    Electricity_6r6kV_3r81kV_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6r6kV_3r81kV_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_6r6kV_3r81kV_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6.6kV-3.81kV-3Ph-60Hz
# 3 Phases


class Electricity_6r6kV_3r81kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6r6kV_3r81kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6r6kV_3r81kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6r6kV_3r81kV_3Ph_60Hz


class Electricity_6r6kV_3r81kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6r6kV_3r81kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6r6kV_3r81kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6r6kV_3r81kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6r6kV_3r81kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6r6kV_3r81kV_3Ph_60Hz


class Electricity_6r6kV_3r81kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_6r6kV_3r81kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6r6kV_3r81kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_6r6kV_3r81kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6.6kV-3Ph-60Hz
# 3 Phases


class Electricity_6r6kV_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6r6kV_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6r6kV_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6r6kV_3Ph_60Hz


class Electricity_6r6kV_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6r6kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6r6kV_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6r6kV_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6r6kV_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6r6kV_3Ph_60Hz


class Electricity_6r6kV_3Ph_60HzSystemInletConnectionPoint(
    Electricity_6r6kV_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6r6kV_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_6r6kV_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-600V-1Ph-60Hz
# 1 phase


class Electricity_600V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC600V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_600V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC600V_1Ph_60Hz


class Electricity_600V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_600V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_600V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_600V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_600V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC600V_1Ph_60Hz


class Electricity_600V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_600V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_600V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_600V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-600V-347V-1Ph-60Hz
# 1 phase


class Electricity_600V_347V_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC600V_347V_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_600V_347V_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC600V_347V_1Ph_60Hz


class Electricity_600V_347V_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_600V_347V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_600V_347V_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_600V_347V_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_600V_347V_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC600V_347V_1Ph_60Hz


class Electricity_600V_347V_1Ph_60HzSystemInletConnectionPoint(
    Electricity_600V_347V_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_600V_347V_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_600V_347V_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-600V-347V-3Ph-60Hz
# 3 Phases


class Electricity_600V_347V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC600V_347V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_600V_347V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC600V_347V_3Ph_60Hz


class Electricity_600V_347V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_600V_347V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_600V_347V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_600V_347V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_600V_347V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC600V_347V_3Ph_60Hz


class Electricity_600V_347V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_600V_347V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_600V_347V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_600V_347V_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-600V-3Ph-60Hz
# 3 Phases


class Electricity_600V_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC600V_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_600V_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC600V_3Ph_60Hz


class Electricity_600V_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_600V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_600V_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_600V_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_600V_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC600V_3Ph_60Hz


class Electricity_600V_3Ph_60HzSystemInletConnectionPoint(
    Electricity_600V_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_600V_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_600V_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === DC-12V
# DC


class Electricity_12VConnection(Connection):
    hasMedium = Electricity.DC12V
    _class_iri = S223.Connection


class Electricity_12VConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.DC12V


class Electricity_12VInletConnectionPoint(
    InletConnectionPoint, Electricity_12VConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_12VOutletConnectionPoint(
    OutletConnectionPoint, Electricity_12VConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_12VSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.DC12V


class Electricity_12VSystemInletConnectionPoint(
    Electricity_12VSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_12VSystemOutletConnectionPoint(
    Electricity_12VSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === DC-24V
# DC


class Electricity_24VConnection(Connection):
    hasMedium = Electricity.DC24V
    _class_iri = S223.Connection


class Electricity_24VConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.DC24V


class Electricity_24VInletConnectionPoint(
    InletConnectionPoint, Electricity_24VConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_24VOutletConnectionPoint(
    OutletConnectionPoint, Electricity_24VConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_24VSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.DC24V


class Electricity_24VSystemInletConnectionPoint(
    Electricity_24VSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_24VSystemOutletConnectionPoint(
    Electricity_24VSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === DC-380V
# DC


class Electricity_380VConnection(Connection):
    hasMedium = Electricity.DC380V
    _class_iri = S223.Connection


class Electricity_380VConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.DC380V


class Electricity_380VInletConnectionPoint(
    InletConnectionPoint, Electricity_380VConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_380VOutletConnectionPoint(
    OutletConnectionPoint, Electricity_380VConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_380VSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.DC380V


class Electricity_380VSystemInletConnectionPoint(
    Electricity_380VSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_380VSystemOutletConnectionPoint(
    Electricity_380VSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === DC-48V
# DC


class Electricity_48VConnection(Connection):
    hasMedium = Electricity.DC48V
    _class_iri = S223.Connection


class Electricity_48VConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.DC48V


class Electricity_48VInletConnectionPoint(
    InletConnectionPoint, Electricity_48VConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_48VOutletConnectionPoint(
    OutletConnectionPoint, Electricity_48VConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_48VSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.DC48V


class Electricity_48VSystemInletConnectionPoint(
    Electricity_48VSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_48VSystemOutletConnectionPoint(
    Electricity_48VSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === DC-5V
# DC


class Electricity_5VConnection(Connection):
    hasMedium = Electricity.DC5V
    _class_iri = S223.Connection


class Electricity_5VConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.DC5V


class Electricity_5VInletConnectionPoint(
    InletConnectionPoint, Electricity_5VConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_5VOutletConnectionPoint(
    OutletConnectionPoint, Electricity_5VConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_5VSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.DC5V


class Electricity_5VSystemInletConnectionPoint(
    Electricity_5VSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_5VSystemOutletConnectionPoint(
    Electricity_5VSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint
