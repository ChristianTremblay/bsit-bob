from rdflib import Literal, URIRef

from bob.enum import AnalogSignalTypeEnum, BinarySignalTypeEnum, ProtocolEnum
from bob.properties.network import Mbit_per_seconds

from ..core import (
    BOB,
    P223,
    S223,
    BidirectionalConnectionPoint,
    BidirectionalSystemConnectionPoint,
    Connection,
    ConnectionPoint,
    Electricity,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    InletZoneConnectionPoint,
    Medium,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    OutletZoneConnectionPoint,
    SystemConnectionPoint,
    enum,
)

_namespace = BOB


# === GENERAL
class ElectricalConnection(Connection):
    hasMedium: Medium = Electricity
    _class_iri = S223.Connection


class ElectricalConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity


class ElectricalInletConnectionPoint(InletConnectionPoint, ElectricalConnectionPoint):
    _class_iri = S223.InletConnectionPoint


class ElectricalOutletConnectionPoint(OutletConnectionPoint, ElectricalConnectionPoint):
    _class_iri = S223.OutletConnectionPoint


class ElectricalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity


class ElectricalSystemInletConnectionPoint(
    ElectricalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class ElectricalSystemOutletConnectionPoint(
    ElectricalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === 575V 60Hz


class Electricity_575V_60HzConnection(Connection):
    hasMedium = Electricity.AC575V_60Hz
    _class_iri = S223.Connection


class Electricity_575V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC575V_60Hz


class Electricity_575V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_575V_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_575V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_575V_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_575V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC575V_60Hz


class Electricity_575V_60HzSystemInletConnectionPoint(
    Electricity_575V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class Electricity_575V_60HzSystemOutletConnectionPoint(
    Electricity_575V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === 480V 60Hz


class Electricity_480V_60HzConnection(Connection):
    hasMedium = Electricity.AC480V_60Hz
    _class_iri = S223.Connection


class Electricity_480V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC480V_60Hz


class Electricity_480V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480V_60HzConnectionPoint
):
    _class_iri = S223.Electricity_480V_60HzConnectionPoint


class Electricity_480V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480V_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_480V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC480V_60Hz


class Electricity_480V_60HzSystemInletConnectionPoint(
    Electricity_480V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class Electricity_480V_60HzSystemOutletConnectionPoint(
    Electricity_480V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === 347V 60Hz
# 1 phase of 575V


class Electricity_347V_60HzConnection(Connection):
    hasMedium = Electricity.AC347V_60Hz
    _class_iri = S223.Connection


class Electricity_347V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC347V_60Hz


class Electricity_347V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_347V_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_347V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_347V_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_347V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC347V_60Hz


class Electricity_347V_60HzSystemInletConnectionPoint(
    Electricity_347V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class Electricity_347V_60HzSystemOutletConnectionPoint(
    Electricity_347V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === 277V 60Hz
# 1 phase of 480V (US)


class Electricity_277V_60HzConnection(Connection):
    hasMedium = Electricity.AC277V_60Hz
    _class_iri = S223.Connection


class Electricity_277V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC277V_60Hz


class Electricity_277V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_277V_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_277V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_277V_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_277V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC277V_60Hz


class Electricity_277V_60HzSystemInletConnectionPoint(
    Electricity_277V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class Electricity_277V_60HzSystemOutletConnectionPoint(
    Electricity_277V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === 208V 60Hz
# 3 phase


class Electricity_208V_60HzConnection(Connection):
    hasMedium = Electricity.AC208V_60Hz
    _class_iri = S223.Connection


class Electricity_208V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC208V_60Hz


class Electricity_208V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208V_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_208V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208V_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_208V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC208V_60Hz


class Electricity_208V_60HzSystemInletConnectionPoint(
    Electricity_208V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class Electricity_208V_60HzSystemOutletConnectionPoint(
    Electricity_208V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === 120V_240V 60Hz
# Often the output of a transformer feeding a distribution panel
# Includes 2 x 120VAC 60Hz line, a neutral and a ground
# Used together, 2 x 120VAC = 240VAC
# Each phase can be used to provide 120VAC


class Electricity_120V_240V_60HzConnection(Connection):
    hasMedium = Electricity.AC120V_240V_60Hz
    _class_iri = S223.Connection


class Electricity_120V_240V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC120V_240V_60Hz


class Electricity_120V_240V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_120V_240V_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_120V_240V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_120V_240V_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_120V_240V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC120V_240V_60Hz


class lectricity_120V_240V_60HzSystemInletConnectionPoint(
    Electricity_120V_240V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class lectricity_120V_240V_60HzSystemOutletConnectionPoint(
    Electricity_120V_240V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === 240V 60Hz


class Electricity_240V_60HzConnection(Connection):
    hasMedium = Electricity.AC240V_60Hz
    _class_iri = S223.Connection


class Electricity_240V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_60Hz


class Electricity_240V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_240V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_240V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_60Hz


class Electricity_240V_60HzSystemInletConnectionPoint(
    Electricity_240V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class Electricity_240V_60HzSystemOutletConnectionPoint(
    Electricity_240V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === 120V 60Hz


class Electricity_120V_60HzConnection(Connection):
    hasMedium = Electricity.AC120V_60Hz
    _class_iri = S223.Connection


class Electricity_120V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC120V_60Hz


class Electricity_120V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_120V_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_120V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_120V_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_120V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC120V_60Hz


class Electricity_120V_60HzSystemInletConnectionPoint(
    Electricity_120V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class Electricity_120V_60HzSystemOutletConnectionPoint(
    Electricity_120V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === 24V 60Hz


class Electricity_24V_60HzConnection(Connection):
    hasMedium = Electricity.AC24V_60Hz
    _class_iri = S223.Connection


class Electricity_24V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC24V_60Hz


class Electricity_24V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_24V_60HzConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class Electricity_24V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_24V_60HzConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class Electricity_24V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC24V_60Hz


class Electricity_24V_60HzSystemInletConnectionPoint(
    Electricity_24V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class Electricity_24V_60HzSystemOutletConnectionPoint(
    Electricity_24V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


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


# This is high level and we don't know if it's using 120V or 24VAC or 5VDC...
# It is modeling dry contact, Triac and other On-Off relationships

# === GENERAL
class OnOffSignalConnection(Connection):
    hasMedium = Electricity.OnOffSignal
    _class_iri = S223.Connection


class OnOffSignalConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.OnOffSignal
    hasSignalType: BinarySignalTypeEnum


class OnOffSignalInletConnectionPoint(InletConnectionPoint, OnOffSignalConnectionPoint):
    _class_iri = S223.BinaryInput


class OnOffSignalOutletConnectionPoint(
    OutletConnectionPoint, OnOffSignalConnectionPoint
):
    _class_iri = S223.BinaryOutput


class OnOffSignalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.OnOffSignal


class OnOffSignalSystemInletConnectionPoint(
    OnOffSignalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class OnOffSignalSystemOutletConnectionPoint(
    OnOffSignalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# This is high level and we don't know if it's using 0-10VDC, 4-20mA, etc...
# === Modulation signals
class ModulationSignalConnection(Connection):
    hasMedium = Electricity.ModulationSignal
    _class_iri = S223.Connection


class ModulationSignalConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.ModulationSignal
    hasSignalType: AnalogSignalTypeEnum


class ModulationSignalInletConnectionPoint(
    InletConnectionPoint, ModulationSignalConnectionPoint
):
    _class_iri = S223.AnalogInput


class ModulationSignalOutletConnectionPoint(
    OutletConnectionPoint, ModulationSignalConnectionPoint
):
    _class_iri = S223.AnalogOutput


class ModulationSignalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.ModulationSignal


class ModulationSignalSystemInletConnectionPoint(
    ModulationSignalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = S223.InletSystemConnectionPoint


class ModulationSignalSystemOutletConnectionPoint(
    ModulationSignalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = S223.OutletSystemConnectionPoint


# === Networks
class RS485Connection(Connection):
    hasMedium = Electricity.RS485
    _class_iri = S223.Connection


class RS485ConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.RS485
    hasProtocol: ProtocolEnum


class RS485BidirectionalConnectionPoint(
    BidirectionalConnectionPoint, RS485ConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint


class RS485SystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.RS485


class RS485BidirectionalSystemConnectionPoint(
    RS485SystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    _class_iri = S223.BidirectionalSystemConnectionPoint


# === Networks
class EthernetConnection(Connection):
    hasMedium = Electricity.Ethernet
    _class_iri = S223.Connection


class EthernetConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.Ethernet
    hasProtocol: ProtocolEnum
    data_rate: Mbit_per_seconds
    vlan: Literal


class EthernetBidirectionalConnectionPoint(
    BidirectionalConnectionPoint, EthernetConnectionPoint
):
    _class_iri = S223.BidirectionalConnectionPoint


class EthernetSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.Ethernet


class EthernetBidirectionalSystemConnectionPoint(
    EthernetSystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    _class_iri = S223.BidirectionalSystemConnectionPoint
