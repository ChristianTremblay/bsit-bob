from rdflib import URIRef
from ..core import s223, enum

from ..core import (
    Medium,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    InletZoneConnectionPoint,
    OutletZoneConnectionPoint,
)
from ..signal import AnalogIn, AnalogOut

__namespace__ = enum


# === GENERAL
class Electricity(Medium):
    node_type: URIRef = enum["Medium-Electricity"]


class ElectricalConnection(Connection):
    hasMedium: URIRef = Electricity.node_type
    node_type = None


class ElectricalConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Electricity.node_type
    node_type = None


class ElectricalInletConnectionPoint(InletConnectionPoint, ElectricalConnectionPoint):
    node_type = None


class ElectricalOutletConnectionPoint(OutletConnectionPoint, ElectricalConnectionPoint):
    node_type = None


class ElectricalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: URIRef = Electricity.node_type
    node_type = None


class ElectricalSystemInletConnectionPoint(
    ElectricalSystemConnectionPoint, InletSystemConnectionPoint
):
    hasMedium: URIRef = Electricity.node_type
    node_type = None


class ElectricalSystemOutletConnectionPoint(
    ElectricalSystemConnectionPoint, OutletSystemConnectionPoint
):
    hasMedium: URIRef = Electricity.node_type
    node_type = None


# === 575V 60Hz


class Electricity_575V_60Hz(Medium):
    node_type: URIRef = enum["Electricity-575V.60Hz"]


class Electricity_575V_60HzConnection(Connection):
    hasMedium: URIRef = Electricity_575V_60Hz.node_type
    node_type = None


class Electricity_575V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Electricity_575V_60Hz.node_type
    node_type = None


class Electricity_575V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_575V_60HzConnectionPoint
):
    node_type = None


class Electricity_575V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_575V_60HzConnectionPoint
):
    node_type = None


class Electricity_575V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: URIRef = Electricity_575V_60Hz.node_type
    node_type = None


class Electricity_575V_60HzSystemInletConnectionPoint(
    Electricity_575V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    hasMedium: URIRef = Electricity_575V_60Hz.node_type
    node_type = None


class Electricity_575V_60HzSystemOutletConnectionPoint(
    Electricity_575V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    hasMedium: URIRef = Electricity_575V_60Hz.node_type
    node_type = None


# === 120V_240V 60Hz
# Often the output of a transformer feeding a distribution panel
# Includes 2 x 120VAC 60Hz line, a neutral and a ground
# Used together, 2 x 120VAC = 240VAC
# Each phase canbe used to provide 120VAC


class Electricity_120V_240V_60Hz(Medium):
    node_type: URIRef = enum["Electricity-120V_240V.60Hz"]


class Electricity_120V_240V_60HzConnection(Connection):
    hasMedium: URIRef = Electricity_120V_240V_60Hz.node_type
    node_type = None


class Electricity_120V_240V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Electricity_120V_240V_60Hz.node_type
    node_type = None


class Electricity_120V_240V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_120V_240V_60HzConnectionPoint
):
    node_type = None


class Electricity_120V_240V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_120V_240V_60HzConnectionPoint
):
    node_type = None


class Electricity_120V_240V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: URIRef = Electricity_120V_240V_60Hz.node_type
    node_type = None


class lectricity_120V_240V_60HzSystemInletConnectionPoint(
    Electricity_120V_240V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    hasMedium: URIRef = Electricity_120V_240V_60Hz.node_type
    node_type = None


class lectricity_120V_240V_60HzSystemOutletConnectionPoint(
    Electricity_120V_240V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    hasMedium: URIRef = Electricity_120V_240V_60Hz.node_type
    node_type = None


# === 240V 60Hz


class Electricity_240V_60Hz(Medium):
    node_type: URIRef = enum["Electricity-240V.60Hz"]


class Electricity_240V_60HzConnection(Connection):
    hasMedium: URIRef = Electricity_240V_60Hz.node_type
    node_type = None


class Electricity_240V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Electricity_240V_60Hz.node_type
    node_type = None


class Electricity_240V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_60HzConnectionPoint
):
    node_type = None


class Electricity_240V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_60HzConnectionPoint
):
    node_type = None


class Electricity_240V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: URIRef = Electricity_240V_60Hz.node_type
    node_type = None


class lectricity_240V_60HzSystemInletConnectionPoint(
    Electricity_240V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    hasMedium: URIRef = Electricity_240V_60Hz.node_type
    node_type = None


class lectricity_240V_60HzSystemOutletConnectionPoint(
    Electricity_240V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    hasMedium: URIRef = Electricity_240V_60Hz.node_type
    node_type = None


# === 120V 60Hz


class Electricity_120V_60Hz(Medium):
    node_type: URIRef = enum["Electricity-120V.60Hz"]


class Electricity_120V_60HzConnection(Connection):
    hasMedium: URIRef = Electricity_120V_60Hz.node_type
    node_type = None


class Electricity_120V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: URIRef = Electricity_120V_60Hz.node_type
    node_type = None


class Electricity_120V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_120V_60HzConnectionPoint
):
    node_type = None


class Electricity_120V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_120V_60HzConnectionPoint
):
    node_type = None


class Electricity_120V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: URIRef = Electricity_120V_60Hz.node_type
    node_type = None


class Electricity_120V_60HzSystemInletConnectionPoint(
    Electricity_120V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    hasMedium: URIRef = Electricity_120V_60Hz.node_type
    node_type = None


class Electricity_120V_60HzSystemOutletConnectionPoint(
    Electricity_120V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    hasMedium: URIRef = Electricity_120V_60Hz.node_type
    node_type = None


# ISSUE - SEMANTIC
# For electricity... when we'll make the connection, Substance will need to be compatible
# For that we'll need at least
# Electricity-575V.60Hz
# Electricity-480V.60Hz
# Electricity-240V.60Hz
# Electricity-120V.60Hz
# Electricity-24V.60Hz
# Electricity-24V.DC
# Electricity-12V.DC
# and European
