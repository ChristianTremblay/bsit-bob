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


# === AC-10000VLL-1Ph-60Hz
# 1 phase


class Electricity_10000VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC10000VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_10000VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC10000VLL_1Ph_60Hz


class Electricity_10000VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_10000VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_10000VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_10000VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_10000VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC10000VLL_1Ph_60Hz


class Electricity_10000VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_10000VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_10000VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_10000VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-10000VLL-3Ph-60Hz
# 3 Phases


class Electricity_10000VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC10000VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_10000VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC10000VLL_3Ph_60Hz


class Electricity_10000VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_10000VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_10000VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_10000VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_10000VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC10000VLL_3Ph_60Hz


class Electricity_10000VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_10000VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_10000VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_10000VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-10000VLL-5770VLN-1Ph-60Hz
# 1 phase


class Electricity_10000VLL_5770VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC10000VLL_5770VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_10000VLL_5770VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC10000VLL_5770VLN_1Ph_60Hz


class Electricity_10000VLL_5770VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_10000VLL_5770VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_10000VLL_5770VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_10000VLL_5770VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_10000VLL_5770VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC10000VLL_5770VLN_1Ph_60Hz


class Electricity_10000VLL_5770VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_10000VLL_5770VLN_1Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_10000VLL_5770VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_10000VLL_5770VLN_1Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-10000VLL-5770VLN-3Ph-60Hz
# 3 Phases


class Electricity_10000VLL_5770VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC10000VLL_5770VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_10000VLL_5770VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC10000VLL_5770VLN_3Ph_60Hz


class Electricity_10000VLL_5770VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_10000VLL_5770VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_10000VLL_5770VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_10000VLL_5770VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_10000VLL_5770VLN_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC10000VLL_5770VLN_3Ph_60Hz


class Electricity_10000VLL_5770VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_10000VLL_5770VLN_3Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_10000VLL_5770VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_10000VLL_5770VLN_3Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-110VLN-1Ph-50Hz
# 1 phase


class Electricity_110VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC110VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_110VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC110VLN_1Ph_50Hz


class Electricity_110VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_110VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_110VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_110VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_110VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC110VLN_1Ph_50Hz


class Electricity_110VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_110VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_110VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_110VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-120VLN-1Ph-60Hz
# 1 phase


class Electricity_120VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC120VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_120VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC120VLN_1Ph_60Hz


class Electricity_120VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_120VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_120VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_120VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_120VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC120VLN_1Ph_60Hz


class Electricity_120VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_120VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_120VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_120VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-127VLN-1Ph-50Hz
# 1 phase


class Electricity_127VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC127VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_127VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC127VLN_1Ph_50Hz


class Electricity_127VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_127VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_127VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_127VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_127VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC127VLN_1Ph_50Hz


class Electricity_127VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_127VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_127VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_127VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-139VLN-1Ph-50Hz
# 1 phase


class Electricity_139VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC139VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_139VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC139VLN_1Ph_50Hz


class Electricity_139VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_139VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_139VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_139VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_139VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC139VLN_1Ph_50Hz


class Electricity_139VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_139VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_139VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_139VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-1730VLN-1Ph-60Hz
# 1 phase


class Electricity_1730VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC1730VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_1730VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC1730VLN_1Ph_60Hz


class Electricity_1730VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_1730VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_1730VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_1730VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_1730VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC1730VLN_1Ph_60Hz


class Electricity_1730VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_1730VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_1730VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_1730VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-1900VLN-1Ph-60Hz
# 1 phase


class Electricity_1900VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC1900VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_1900VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC1900VLN_1Ph_60Hz


class Electricity_1900VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_1900VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_1900VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_1900VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_1900VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC1900VLN_1Ph_60Hz


class Electricity_1900VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_1900VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_1900VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_1900VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-190VLL-110VLN-1Ph-50Hz
# 1 phase


class Electricity_190VLL_110VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC190VLL_110VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_190VLL_110VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC190VLL_110VLN_1Ph_50Hz


class Electricity_190VLL_110VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_190VLL_110VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_190VLL_110VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_190VLL_110VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_190VLL_110VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC190VLL_110VLN_1Ph_50Hz


class Electricity_190VLL_110VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_190VLL_110VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_190VLL_110VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_190VLL_110VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-190VLL-110VLN-3Ph-50Hz
# 3 Phases


class Electricity_190VLL_110VLN_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC190VLL_110VLN_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_190VLL_110VLN_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC190VLL_110VLN_3Ph_50Hz


class Electricity_190VLL_110VLN_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_190VLL_110VLN_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_190VLL_110VLN_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_190VLL_110VLN_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_190VLL_110VLN_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC190VLL_110VLN_3Ph_50Hz


class Electricity_190VLL_110VLN_3Ph_50HzSystemInletConnectionPoint(
    Electricity_190VLL_110VLN_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_190VLL_110VLN_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_190VLL_110VLN_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-190VLL-1Ph-50Hz
# 1 phase


class Electricity_190VLL_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC190VLL_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_190VLL_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC190VLL_1Ph_50Hz


class Electricity_190VLL_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_190VLL_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_190VLL_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_190VLL_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_190VLL_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC190VLL_1Ph_50Hz


class Electricity_190VLL_1Ph_50HzSystemInletConnectionPoint(
    Electricity_190VLL_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_190VLL_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_190VLL_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-190VLL-3Ph-50Hz
# 3 Phases


class Electricity_190VLL_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC190VLL_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_190VLL_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC190VLL_3Ph_50Hz


class Electricity_190VLL_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_190VLL_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_190VLL_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_190VLL_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_190VLL_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC190VLL_3Ph_50Hz


class Electricity_190VLL_3Ph_50HzSystemInletConnectionPoint(
    Electricity_190VLL_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_190VLL_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_190VLL_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-208VLL-120VLN-1Ph-60Hz
# 1 phase


class Electricity_208VLL_120VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC208VLL_120VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_208VLL_120VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC208VLL_120VLN_1Ph_60Hz


class Electricity_208VLL_120VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208VLL_120VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_208VLL_120VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208VLL_120VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_208VLL_120VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC208VLL_120VLN_1Ph_60Hz


class Electricity_208VLL_120VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_208VLL_120VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_208VLL_120VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_208VLL_120VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-208VLL-120VLN-3Ph-60Hz
# 3 Phases


class Electricity_208VLL_120VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC208VLL_120VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_208VLL_120VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC208VLL_120VLN_3Ph_60Hz


class Electricity_208VLL_120VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208VLL_120VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_208VLL_120VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208VLL_120VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_208VLL_120VLN_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC208VLL_120VLN_3Ph_60Hz


class Electricity_208VLL_120VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_208VLL_120VLN_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_208VLL_120VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_208VLL_120VLN_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-208VLL-1Ph-60Hz
# 1 phase


class Electricity_208VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC208VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_208VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC208VLL_1Ph_60Hz


class Electricity_208VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_208VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_208VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC208VLL_1Ph_60Hz


class Electricity_208VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_208VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_208VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_208VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-208VLL-3Ph-60Hz
# 3 Phases


class Electricity_208VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC208VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_208VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC208VLL_3Ph_60Hz


class Electricity_208VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_208VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_208VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC208VLL_3Ph_60Hz


class Electricity_208VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_208VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_208VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_208VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-219VLN-1Ph-60Hz
# 1 phase


class Electricity_219VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC219VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_219VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC219VLN_1Ph_60Hz


class Electricity_219VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_219VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_219VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_219VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_219VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC219VLN_1Ph_60Hz


class Electricity_219VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_219VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_219VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_219VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-220VLL-127VLN-1Ph-50Hz
# 1 phase


class Electricity_220VLL_127VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC220VLL_127VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_220VLL_127VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC220VLL_127VLN_1Ph_50Hz


class Electricity_220VLL_127VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_220VLL_127VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_220VLL_127VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_220VLL_127VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_220VLL_127VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC220VLL_127VLN_1Ph_50Hz


class Electricity_220VLL_127VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_220VLL_127VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_220VLL_127VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_220VLL_127VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-220VLL-127VLN-3Ph-50Hz
# 3 Phases


class Electricity_220VLL_127VLN_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC220VLL_127VLN_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_220VLL_127VLN_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC220VLL_127VLN_3Ph_50Hz


class Electricity_220VLL_127VLN_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_220VLL_127VLN_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_220VLL_127VLN_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_220VLL_127VLN_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_220VLL_127VLN_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC220VLL_127VLN_3Ph_50Hz


class Electricity_220VLL_127VLN_3Ph_50HzSystemInletConnectionPoint(
    Electricity_220VLL_127VLN_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_220VLL_127VLN_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_220VLL_127VLN_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-220VLL-1Ph-50Hz
# 1 phase


class Electricity_220VLL_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC220VLL_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_220VLL_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC220VLL_1Ph_50Hz


class Electricity_220VLL_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_220VLL_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_220VLL_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_220VLL_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_220VLL_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC220VLL_1Ph_50Hz


class Electricity_220VLL_1Ph_50HzSystemInletConnectionPoint(
    Electricity_220VLL_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_220VLL_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_220VLL_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-220VLL-3Ph-50Hz
# 3 Phases


class Electricity_220VLL_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC220VLL_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_220VLL_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC220VLL_3Ph_50Hz


class Electricity_220VLL_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_220VLL_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_220VLL_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_220VLL_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_220VLL_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC220VLL_3Ph_50Hz


class Electricity_220VLL_3Ph_50HzSystemInletConnectionPoint(
    Electricity_220VLL_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_220VLL_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_220VLL_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-231VLN-1Ph-50Hz
# 1 phase


class Electricity_231VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC231VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_231VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC231VLN_1Ph_50Hz


class Electricity_231VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_231VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_231VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_231VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_231VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC231VLN_1Ph_50Hz


class Electricity_231VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_231VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_231VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_231VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-2400VLN-1Ph-60Hz
# 1 phase


class Electricity_2400VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC2400VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_2400VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC2400VLN_1Ph_60Hz


class Electricity_2400VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_2400VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_2400VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_2400VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_2400VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC2400VLN_1Ph_60Hz


class Electricity_2400VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_2400VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_2400VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_2400VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240VLL-120VLN-1Ph-60Hz
# 1 phase


class Electricity_240VLL_120VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240VLL_120VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240VLL_120VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240VLL_120VLN_1Ph_60Hz


class Electricity_240VLL_120VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240VLL_120VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240VLL_120VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240VLL_120VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240VLL_120VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240VLL_120VLN_1Ph_60Hz


class Electricity_240VLL_120VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_240VLL_120VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240VLL_120VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_240VLL_120VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240VLL-139VLN-1Ph-50Hz
# 1 phase


class Electricity_240VLL_139VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC240VLL_139VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_240VLL_139VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240VLL_139VLN_1Ph_50Hz


class Electricity_240VLL_139VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240VLL_139VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240VLL_139VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240VLL_139VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240VLL_139VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240VLL_139VLN_1Ph_50Hz


class Electricity_240VLL_139VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_240VLL_139VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240VLL_139VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_240VLL_139VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240VLL-139VLN-3Ph-50Hz
# 3 Phases


class Electricity_240VLL_139VLN_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC240VLL_139VLN_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_240VLL_139VLN_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240VLL_139VLN_3Ph_50Hz


class Electricity_240VLL_139VLN_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240VLL_139VLN_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240VLL_139VLN_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240VLL_139VLN_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240VLL_139VLN_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240VLL_139VLN_3Ph_50Hz


class Electricity_240VLL_139VLN_3Ph_50HzSystemInletConnectionPoint(
    Electricity_240VLL_139VLN_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240VLL_139VLN_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_240VLL_139VLN_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240VLL-1Ph-50Hz
# 1 phase


class Electricity_240VLL_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC240VLL_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_240VLL_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240VLL_1Ph_50Hz


class Electricity_240VLL_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240VLL_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240VLL_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240VLL_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240VLL_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240VLL_1Ph_50Hz


class Electricity_240VLL_1Ph_50HzSystemInletConnectionPoint(
    Electricity_240VLL_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240VLL_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_240VLL_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240VLL-1Ph-60Hz
# 1 phase


class Electricity_240VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240VLL_1Ph_60Hz


class Electricity_240VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240VLL_1Ph_60Hz


class Electricity_240VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_240VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_240VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240VLL-208VLN-120VLN-1Ph-60Hz
# 1 phase


class Electricity_240VLL_208VLN_120VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240VLL_208VLN_120VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240VLL_208VLN_120VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240VLL_208VLN_120VLN_1Ph_60Hz


class Electricity_240VLL_208VLN_120VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240VLL_208VLN_120VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240VLL_208VLN_120VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240VLL_208VLN_120VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240VLL_208VLN_120VLN_1Ph_60HzSystemConnectionPoint(
    SystemConnectionPoint
):
    hasMedium = Electricity.AC240VLL_208VLN_120VLN_1Ph_60Hz


class Electricity_240VLL_208VLN_120VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_240VLL_208VLN_120VLN_1Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240VLL_208VLN_120VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_240VLL_208VLN_120VLN_1Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240VLL-208VLN-120VLN-3Ph-60Hz
# 3 Phases


class Electricity_240VLL_208VLN_120VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240VLL_208VLN_120VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240VLL_208VLN_120VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240VLL_208VLN_120VLN_3Ph_60Hz


class Electricity_240VLL_208VLN_120VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240VLL_208VLN_120VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240VLL_208VLN_120VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240VLL_208VLN_120VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240VLL_208VLN_120VLN_3Ph_60HzSystemConnectionPoint(
    SystemConnectionPoint
):
    hasMedium = Electricity.AC240VLL_208VLN_120VLN_3Ph_60Hz


class Electricity_240VLL_208VLN_120VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_240VLL_208VLN_120VLN_3Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240VLL_208VLN_120VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_240VLL_208VLN_120VLN_3Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240VLL-3Ph-50Hz
# 3 Phases


class Electricity_240VLL_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC240VLL_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_240VLL_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240VLL_3Ph_50Hz


class Electricity_240VLL_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240VLL_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240VLL_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240VLL_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240VLL_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240VLL_3Ph_50Hz


class Electricity_240VLL_3Ph_50HzSystemInletConnectionPoint(
    Electricity_240VLL_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240VLL_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_240VLL_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240VLL-3Ph-60Hz
# 3 Phases


class Electricity_240VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC240VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_240VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240VLL_3Ph_60Hz


class Electricity_240VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240VLL_3Ph_60Hz


class Electricity_240VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_240VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_240VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-240VLN-1Ph-50Hz
# 1 phase


class Electricity_240VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC240VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_240VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240VLN_1Ph_50Hz


class Electricity_240VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240VLN_1Ph_50Hz


class Electricity_240VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_240VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_240VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_240VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-24VLN-1Ph-50Hz
# 1 phase


class Electricity_24VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC24VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_24VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC24VLN_1Ph_50Hz


class Electricity_24VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_24VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_24VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_24VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_24VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC24VLN_1Ph_50Hz


class Electricity_24VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_24VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_24VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_24VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-24VLN-1Ph-60Hz
# 1 phase


class Electricity_24VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC24VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_24VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC24VLN_1Ph_60Hz


class Electricity_24VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_24VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_24VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_24VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_24VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC24VLN_1Ph_60Hz


class Electricity_24VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_24VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_24VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_24VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-277VLN-1Ph-60Hz
# 1 phase


class Electricity_277VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC277VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_277VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC277VLN_1Ph_60Hz


class Electricity_277VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_277VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_277VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_277VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_277VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC277VLN_1Ph_60Hz


class Electricity_277VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_277VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_277VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_277VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3000VLL-1730VLN-1Ph-60Hz
# 1 phase


class Electricity_3000VLL_1730VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3000VLL_1730VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3000VLL_1730VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3000VLL_1730VLN_1Ph_60Hz


class Electricity_3000VLL_1730VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3000VLL_1730VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3000VLL_1730VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3000VLL_1730VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3000VLL_1730VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3000VLL_1730VLN_1Ph_60Hz


class Electricity_3000VLL_1730VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_3000VLL_1730VLN_1Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3000VLL_1730VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_3000VLL_1730VLN_1Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3000VLL-1730VLN-3Ph-60Hz
# 3 Phases


class Electricity_3000VLL_1730VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3000VLL_1730VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3000VLL_1730VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3000VLL_1730VLN_3Ph_60Hz


class Electricity_3000VLL_1730VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3000VLL_1730VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3000VLL_1730VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3000VLL_1730VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3000VLL_1730VLN_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3000VLL_1730VLN_3Ph_60Hz


class Electricity_3000VLL_1730VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_3000VLL_1730VLN_3Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3000VLL_1730VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_3000VLL_1730VLN_3Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3000VLL-1Ph-60Hz
# 1 phase


class Electricity_3000VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3000VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3000VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3000VLL_1Ph_60Hz


class Electricity_3000VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3000VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3000VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3000VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3000VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3000VLL_1Ph_60Hz


class Electricity_3000VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_3000VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3000VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_3000VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3000VLL-3Ph-60Hz
# 3 Phases


class Electricity_3000VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3000VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3000VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3000VLL_3Ph_60Hz


class Electricity_3000VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3000VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3000VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3000VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3000VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3000VLL_3Ph_60Hz


class Electricity_3000VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_3000VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3000VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_3000VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3300VLL-1900VLN-1Ph-60Hz
# 1 phase


class Electricity_3300VLL_1900VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3300VLL_1900VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3300VLL_1900VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3300VLL_1900VLN_1Ph_60Hz


class Electricity_3300VLL_1900VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3300VLL_1900VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3300VLL_1900VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3300VLL_1900VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3300VLL_1900VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3300VLL_1900VLN_1Ph_60Hz


class Electricity_3300VLL_1900VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_3300VLL_1900VLN_1Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3300VLL_1900VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_3300VLL_1900VLN_1Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3300VLL-1900VLN-3Ph-60Hz
# 3 Phases


class Electricity_3300VLL_1900VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3300VLL_1900VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3300VLL_1900VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3300VLL_1900VLN_3Ph_60Hz


class Electricity_3300VLL_1900VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3300VLL_1900VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3300VLL_1900VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3300VLL_1900VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3300VLL_1900VLN_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3300VLL_1900VLN_3Ph_60Hz


class Electricity_3300VLL_1900VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_3300VLL_1900VLN_3Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3300VLL_1900VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_3300VLL_1900VLN_3Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3300VLL-1Ph-60Hz
# 1 phase


class Electricity_3300VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3300VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3300VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3300VLL_1Ph_60Hz


class Electricity_3300VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3300VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3300VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3300VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3300VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3300VLL_1Ph_60Hz


class Electricity_3300VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_3300VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3300VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_3300VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3300VLL-3Ph-60Hz
# 3 Phases


class Electricity_3300VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3300VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3300VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3300VLL_3Ph_60Hz


class Electricity_3300VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3300VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3300VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3300VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3300VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3300VLL_3Ph_60Hz


class Electricity_3300VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_3300VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3300VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_3300VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3460VLN-1Ph-60Hz
# 1 phase


class Electricity_3460VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3460VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3460VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3460VLN_1Ph_60Hz


class Electricity_3460VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3460VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3460VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3460VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3460VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3460VLN_1Ph_60Hz


class Electricity_3460VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_3460VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3460VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_3460VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-347VLN-1Ph-60Hz
# 1 phase


class Electricity_347VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC347VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_347VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC347VLN_1Ph_60Hz


class Electricity_347VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_347VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_347VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_347VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_347VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC347VLN_1Ph_60Hz


class Electricity_347VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_347VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_347VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_347VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-380VLL-1Ph-60Hz
# 1 phase


class Electricity_380VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC380VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_380VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC380VLL_1Ph_60Hz


class Electricity_380VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_380VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_380VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_380VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_380VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC380VLL_1Ph_60Hz


class Electricity_380VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_380VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_380VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_380VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-380VLL-219VLN-1Ph-60Hz
# 1 phase


class Electricity_380VLL_219VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC380VLL_219VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_380VLL_219VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC380VLL_219VLN_1Ph_60Hz


class Electricity_380VLL_219VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_380VLL_219VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_380VLL_219VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_380VLL_219VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_380VLL_219VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC380VLL_219VLN_1Ph_60Hz


class Electricity_380VLL_219VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_380VLL_219VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_380VLL_219VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_380VLL_219VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-380VLL-219VLN-3Ph-60Hz
# 3 Phases


class Electricity_380VLL_219VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC380VLL_219VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_380VLL_219VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC380VLL_219VLN_3Ph_60Hz


class Electricity_380VLL_219VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_380VLL_219VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_380VLL_219VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_380VLL_219VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_380VLL_219VLN_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC380VLL_219VLN_3Ph_60Hz


class Electricity_380VLL_219VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_380VLL_219VLN_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_380VLL_219VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_380VLL_219VLN_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-380VLL-3Ph-60Hz
# 3 Phases


class Electricity_380VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC380VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_380VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC380VLL_3Ph_60Hz


class Electricity_380VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_380VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_380VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_380VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_380VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC380VLL_3Ph_60Hz


class Electricity_380VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_380VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_380VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_380VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-3810VLN-1Ph-60Hz
# 1 phase


class Electricity_3810VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC3810VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_3810VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC3810VLN_1Ph_60Hz


class Electricity_3810VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_3810VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_3810VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_3810VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_3810VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC3810VLN_1Ph_60Hz


class Electricity_3810VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_3810VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_3810VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_3810VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-400VLL-1Ph-50Hz
# 1 phase


class Electricity_400VLL_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC400VLL_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_400VLL_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC400VLL_1Ph_50Hz


class Electricity_400VLL_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_400VLL_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_400VLL_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_400VLL_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_400VLL_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC400VLL_1Ph_50Hz


class Electricity_400VLL_1Ph_50HzSystemInletConnectionPoint(
    Electricity_400VLL_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_400VLL_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_400VLL_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-400VLL-231VLN-1Ph-50Hz
# 1 phase


class Electricity_400VLL_231VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC400VLL_231VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_400VLL_231VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC400VLL_231VLN_1Ph_50Hz


class Electricity_400VLL_231VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_400VLL_231VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_400VLL_231VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_400VLL_231VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_400VLL_231VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC400VLL_231VLN_1Ph_50Hz


class Electricity_400VLL_231VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_400VLL_231VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_400VLL_231VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_400VLL_231VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-400VLL-231VLN-3Ph-50Hz
# 3 Phases


class Electricity_400VLL_231VLN_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC400VLL_231VLN_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_400VLL_231VLN_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC400VLL_231VLN_3Ph_50Hz


class Electricity_400VLL_231VLN_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_400VLL_231VLN_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_400VLL_231VLN_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_400VLL_231VLN_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_400VLL_231VLN_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC400VLL_231VLN_3Ph_50Hz


class Electricity_400VLL_231VLN_3Ph_50HzSystemInletConnectionPoint(
    Electricity_400VLL_231VLN_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_400VLL_231VLN_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_400VLL_231VLN_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-400VLL-3Ph-50Hz
# 3 Phases


class Electricity_400VLL_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC400VLL_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_400VLL_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC400VLL_3Ph_50Hz


class Electricity_400VLL_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_400VLL_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_400VLL_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_400VLL_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_400VLL_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC400VLL_3Ph_50Hz


class Electricity_400VLL_3Ph_50HzSystemInletConnectionPoint(
    Electricity_400VLL_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_400VLL_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_400VLL_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-415VLL-1Ph-50Hz
# 1 phase


class Electricity_415VLL_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC415VLL_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_415VLL_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC415VLL_1Ph_50Hz


class Electricity_415VLL_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_415VLL_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_415VLL_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_415VLL_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_415VLL_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC415VLL_1Ph_50Hz


class Electricity_415VLL_1Ph_50HzSystemInletConnectionPoint(
    Electricity_415VLL_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_415VLL_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_415VLL_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-415VLL-240VLN-1Ph-50Hz
# 1 phase


class Electricity_415VLL_240VLN_1Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC415VLL_240VLN_1Ph_50Hz
    _class_iri = S223.Connection


class Electricity_415VLL_240VLN_1Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC415VLL_240VLN_1Ph_50Hz


class Electricity_415VLL_240VLN_1Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_415VLL_240VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_415VLL_240VLN_1Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_415VLL_240VLN_1Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_415VLL_240VLN_1Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC415VLL_240VLN_1Ph_50Hz


class Electricity_415VLL_240VLN_1Ph_50HzSystemInletConnectionPoint(
    Electricity_415VLL_240VLN_1Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_415VLL_240VLN_1Ph_50HzSystemOutletConnectionPoint(
    Electricity_415VLL_240VLN_1Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-415VLL-240VLN-3Ph-50Hz
# 3 Phases


class Electricity_415VLL_240VLN_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC415VLL_240VLN_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_415VLL_240VLN_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC415VLL_240VLN_3Ph_50Hz


class Electricity_415VLL_240VLN_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_415VLL_240VLN_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_415VLL_240VLN_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_415VLL_240VLN_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_415VLL_240VLN_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC415VLL_240VLN_3Ph_50Hz


class Electricity_415VLL_240VLN_3Ph_50HzSystemInletConnectionPoint(
    Electricity_415VLL_240VLN_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_415VLL_240VLN_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_415VLL_240VLN_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-415VLL-3Ph-50Hz
# 3 Phases


class Electricity_415VLL_3Ph_50HzConnection(Connection):
    hasMedium = Electricity.AC415VLL_3Ph_50Hz
    _class_iri = S223.Connection


class Electricity_415VLL_3Ph_50HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC415VLL_3Ph_50Hz


class Electricity_415VLL_3Ph_50HzInletConnectionPoint(
    InletConnectionPoint, Electricity_415VLL_3Ph_50HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_415VLL_3Ph_50HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_415VLL_3Ph_50HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_415VLL_3Ph_50HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC415VLL_3Ph_50Hz


class Electricity_415VLL_3Ph_50HzSystemInletConnectionPoint(
    Electricity_415VLL_3Ph_50HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_415VLL_3Ph_50HzSystemOutletConnectionPoint(
    Electricity_415VLL_3Ph_50HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-4160VLL-1Ph-60Hz
# 1 phase


class Electricity_4160VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC4160VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_4160VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC4160VLL_1Ph_60Hz


class Electricity_4160VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_4160VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_4160VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_4160VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_4160VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC4160VLL_1Ph_60Hz


class Electricity_4160VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_4160VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_4160VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_4160VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-4160VLL-2400VLN-1Ph-60Hz
# 1 phase


class Electricity_4160VLL_2400VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC4160VLL_2400VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_4160VLL_2400VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC4160VLL_2400VLN_1Ph_60Hz


class Electricity_4160VLL_2400VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_4160VLL_2400VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_4160VLL_2400VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_4160VLL_2400VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_4160VLL_2400VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC4160VLL_2400VLN_1Ph_60Hz


class Electricity_4160VLL_2400VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_4160VLL_2400VLN_1Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_4160VLL_2400VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_4160VLL_2400VLN_1Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-4160VLL-2400VLN-3Ph-60Hz
# 3 Phases


class Electricity_4160VLL_2400VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC4160VLL_2400VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_4160VLL_2400VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC4160VLL_2400VLN_3Ph_60Hz


class Electricity_4160VLL_2400VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_4160VLL_2400VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_4160VLL_2400VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_4160VLL_2400VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_4160VLL_2400VLN_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC4160VLL_2400VLN_3Ph_60Hz


class Electricity_4160VLL_2400VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_4160VLL_2400VLN_3Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_4160VLL_2400VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_4160VLL_2400VLN_3Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-4160VLL-3Ph-60Hz
# 3 Phases


class Electricity_4160VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC4160VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_4160VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC4160VLL_3Ph_60Hz


class Electricity_4160VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_4160VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_4160VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_4160VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_4160VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC4160VLL_3Ph_60Hz


class Electricity_4160VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_4160VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_4160VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_4160VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-480VLL-1Ph-60Hz
# 1 phase


class Electricity_480VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC480VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_480VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC480VLL_1Ph_60Hz


class Electricity_480VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_480VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_480VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC480VLL_1Ph_60Hz


class Electricity_480VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_480VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_480VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_480VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-480VLL-277VLN-1Ph-60Hz
# 1 phase


class Electricity_480VLL_277VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC480VLL_277VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_480VLL_277VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC480VLL_277VLN_1Ph_60Hz


class Electricity_480VLL_277VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480VLL_277VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_480VLL_277VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480VLL_277VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_480VLL_277VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC480VLL_277VLN_1Ph_60Hz


class Electricity_480VLL_277VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_480VLL_277VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_480VLL_277VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_480VLL_277VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-480VLL-277VLN-3Ph-60Hz
# 3 Phases


class Electricity_480VLL_277VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC480VLL_277VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_480VLL_277VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC480VLL_277VLN_3Ph_60Hz


class Electricity_480VLL_277VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480VLL_277VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_480VLL_277VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480VLL_277VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_480VLL_277VLN_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC480VLL_277VLN_3Ph_60Hz


class Electricity_480VLL_277VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_480VLL_277VLN_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_480VLL_277VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_480VLL_277VLN_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-480VLL-3Ph-60Hz
# 3 Phases


class Electricity_480VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC480VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_480VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC480VLL_3Ph_60Hz


class Electricity_480VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_480VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_480VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC480VLL_3Ph_60Hz


class Electricity_480VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_480VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_480VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_480VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-5770VLN-1Ph-60Hz
# 1 phase


class Electricity_5770VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC5770VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_5770VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC5770VLN_1Ph_60Hz


class Electricity_5770VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_5770VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_5770VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_5770VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_5770VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC5770VLN_1Ph_60Hz


class Electricity_5770VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_5770VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_5770VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_5770VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6000VLL-1Ph-60Hz
# 1 phase


class Electricity_6000VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6000VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6000VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6000VLL_1Ph_60Hz


class Electricity_6000VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6000VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6000VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6000VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6000VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6000VLL_1Ph_60Hz


class Electricity_6000VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_6000VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6000VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_6000VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6000VLL-3460VLN-1Ph-60Hz
# 1 phase


class Electricity_6000VLL_3460VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6000VLL_3460VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6000VLL_3460VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6000VLL_3460VLN_1Ph_60Hz


class Electricity_6000VLL_3460VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6000VLL_3460VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6000VLL_3460VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6000VLL_3460VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6000VLL_3460VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6000VLL_3460VLN_1Ph_60Hz


class Electricity_6000VLL_3460VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_6000VLL_3460VLN_1Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6000VLL_3460VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_6000VLL_3460VLN_1Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6000VLL-3460VLN-3Ph-60Hz
# 3 Phases


class Electricity_6000VLL_3460VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6000VLL_3460VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6000VLL_3460VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6000VLL_3460VLN_3Ph_60Hz


class Electricity_6000VLL_3460VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6000VLL_3460VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6000VLL_3460VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6000VLL_3460VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6000VLL_3460VLN_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6000VLL_3460VLN_3Ph_60Hz


class Electricity_6000VLL_3460VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_6000VLL_3460VLN_3Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6000VLL_3460VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_6000VLL_3460VLN_3Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6000VLL-3Ph-60Hz
# 3 Phases


class Electricity_6000VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6000VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6000VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6000VLL_3Ph_60Hz


class Electricity_6000VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6000VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6000VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6000VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6000VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6000VLL_3Ph_60Hz


class Electricity_6000VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_6000VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6000VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_6000VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-600VLL-1Ph-60Hz
# 1 phase


class Electricity_600VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC600VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_600VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC600VLL_1Ph_60Hz


class Electricity_600VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_600VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_600VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_600VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_600VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC600VLL_1Ph_60Hz


class Electricity_600VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_600VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_600VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_600VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-600VLL-347VLN-1Ph-60Hz
# 1 phase


class Electricity_600VLL_347VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC600VLL_347VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_600VLL_347VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC600VLL_347VLN_1Ph_60Hz


class Electricity_600VLL_347VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_600VLL_347VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_600VLL_347VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_600VLL_347VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_600VLL_347VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC600VLL_347VLN_1Ph_60Hz


class Electricity_600VLL_347VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_600VLL_347VLN_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_600VLL_347VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_600VLL_347VLN_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-600VLL-347VLN-3Ph-60Hz
# 3 Phases


class Electricity_600VLL_347VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC600VLL_347VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_600VLL_347VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC600VLL_347VLN_3Ph_60Hz


class Electricity_600VLL_347VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_600VLL_347VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_600VLL_347VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_600VLL_347VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_600VLL_347VLN_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC600VLL_347VLN_3Ph_60Hz


class Electricity_600VLL_347VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_600VLL_347VLN_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_600VLL_347VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_600VLL_347VLN_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-600VLL-3Ph-60Hz
# 3 Phases


class Electricity_600VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC600VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_600VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC600VLL_3Ph_60Hz


class Electricity_600VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_600VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_600VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_600VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_600VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC600VLL_3Ph_60Hz


class Electricity_600VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_600VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_600VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_600VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6600VLL-1Ph-60Hz
# 1 phase


class Electricity_6600VLL_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6600VLL_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6600VLL_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6600VLL_1Ph_60Hz


class Electricity_6600VLL_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6600VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6600VLL_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6600VLL_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6600VLL_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6600VLL_1Ph_60Hz


class Electricity_6600VLL_1Ph_60HzSystemInletConnectionPoint(
    Electricity_6600VLL_1Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6600VLL_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_6600VLL_1Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6600VLL-3810VLN-1Ph-60Hz
# 1 phase


class Electricity_6600VLL_3810VLN_1Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6600VLL_3810VLN_1Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6600VLL_3810VLN_1Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6600VLL_3810VLN_1Ph_60Hz


class Electricity_6600VLL_3810VLN_1Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6600VLL_3810VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6600VLL_3810VLN_1Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6600VLL_3810VLN_1Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6600VLL_3810VLN_1Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6600VLL_3810VLN_1Ph_60Hz


class Electricity_6600VLL_3810VLN_1Ph_60HzSystemInletConnectionPoint(
    Electricity_6600VLL_3810VLN_1Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6600VLL_3810VLN_1Ph_60HzSystemOutletConnectionPoint(
    Electricity_6600VLL_3810VLN_1Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6600VLL-3810VLN-3Ph-60Hz
# 3 Phases


class Electricity_6600VLL_3810VLN_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6600VLL_3810VLN_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6600VLL_3810VLN_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6600VLL_3810VLN_3Ph_60Hz


class Electricity_6600VLL_3810VLN_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6600VLL_3810VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6600VLL_3810VLN_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6600VLL_3810VLN_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6600VLL_3810VLN_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6600VLL_3810VLN_3Ph_60Hz


class Electricity_6600VLL_3810VLN_3Ph_60HzSystemInletConnectionPoint(
    Electricity_6600VLL_3810VLN_3Ph_60HzSystemConnectionPoint,
    InletSystemConnectionPoint,
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6600VLL_3810VLN_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_6600VLL_3810VLN_3Ph_60HzSystemConnectionPoint,
    OutletSystemConnectionPoint,
):
    _class_iri = BOB.OutletSystemConnectionPoint


# === AC-6600VLL-3Ph-60Hz
# 3 Phases


class Electricity_6600VLL_3Ph_60HzConnection(Connection):
    hasMedium = Electricity.AC6600VLL_3Ph_60Hz
    _class_iri = S223.Connection


class Electricity_6600VLL_3Ph_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC6600VLL_3Ph_60Hz


class Electricity_6600VLL_3Ph_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_6600VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6600VLL_3Ph_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6600VLL_3Ph_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6600VLL_3Ph_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC6600VLL_3Ph_60Hz


class Electricity_6600VLL_3Ph_60HzSystemInletConnectionPoint(
    Electricity_6600VLL_3Ph_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6600VLL_3Ph_60HzSystemOutletConnectionPoint(
    Electricity_6600VLL_3Ph_60HzSystemConnectionPoint, OutletSystemConnectionPoint
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


# === DC-6V
# DC


class Electricity_6VConnection(Connection):
    hasMedium = Electricity.DC6V
    _class_iri = S223.Connection


class Electricity_6VConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.DC6V


class Electricity_6VInletConnectionPoint(
    InletConnectionPoint, Electricity_6VConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_6VOutletConnectionPoint(
    OutletConnectionPoint, Electricity_6VConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_6VSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.DC6V


class Electricity_6VSystemInletConnectionPoint(
    Electricity_6VSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class Electricity_6VSystemOutletConnectionPoint(
    Electricity_6VSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint
