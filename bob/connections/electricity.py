from rdflib import URIRef

from ..core import (
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
    s223,
)

_namespace = s223


# === GENERAL
class ElectricalConnection(Connection):
    hasMedium: Medium = Electricity
    _class_iri = None


class ElectricalConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity
    _class_iri = None


class ElectricalInletConnectionPoint(InletConnectionPoint, ElectricalConnectionPoint):
    _class_iri = None


class ElectricalOutletConnectionPoint(OutletConnectionPoint, ElectricalConnectionPoint):
    _class_iri = None


class ElectricalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity
    _class_iri = None


class ElectricalSystemInletConnectionPoint(
    ElectricalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class ElectricalSystemOutletConnectionPoint(
    ElectricalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# === 575V 60Hz


class Electricity_575V_60HzConnection(Connection):
    hasMedium = Electricity.AC575V_60Hz
    _class_iri = None


class Electricity_575V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC575V_60Hz
    _class_iri = None


class Electricity_575V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_575V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_575V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_575V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_575V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC575V_60Hz
    _class_iri = None


class Electricity_575V_60HzSystemInletConnectionPoint(
    Electricity_575V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class Electricity_575V_60HzSystemOutletConnectionPoint(
    Electricity_575V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# === 480V 60Hz


class Electricity_480V_60HzConnection(Connection):
    hasMedium = Electricity.AC480V_60Hz
    _class_iri = None


class Electricity_480V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC480V_60Hz
    _class_iri = None


class Electricity_480V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_480V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_480V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC480V_60Hz
    _class_iri = None


class Electricity_480V_60HzSystemInletConnectionPoint(
    Electricity_480V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class Electricity_480V_60HzSystemOutletConnectionPoint(
    Electricity_480V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# === 347V 60Hz
# 1 phase of 575V


class Electricity_347V_60HzConnection(Connection):
    hasMedium = Electricity.AC347V_60Hz
    _class_iri = None


class Electricity_347V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC347V_60Hz
    _class_iri = None


class Electricity_347V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_347V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_347V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_347V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_347V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC347V_60Hz
    _class_iri = None


class Electricity_347V_60HzSystemInletConnectionPoint(
    Electricity_347V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class Electricity_347V_60HzSystemOutletConnectionPoint(
    Electricity_347V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# === 277V 60Hz
# 1 phase of 480V (US)


class Electricity_277V_60HzConnection(Connection):
    hasMedium = Electricity.AC277V_60Hz
    _class_iri = None


class Electricity_277V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC277V_60Hz
    _class_iri = None


class Electricity_277V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_277V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_277V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_277V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_277V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC277V_60Hz
    _class_iri = None


class Electricity_277V_60HzSystemInletConnectionPoint(
    Electricity_277V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class Electricity_277V_60HzSystemOutletConnectionPoint(
    Electricity_277V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# === 208V 60Hz
# 3 phase


class Electricity_208V_60HzConnection(Connection):
    hasMedium = Electricity.AC208V_60Hz
    _class_iri = None


class Electricity_208V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC208V_60Hz
    _class_iri = None


class Electricity_208V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_208V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_208V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC208V_60Hz
    _class_iri = None


class Electricity_208V_60HzSystemInletConnectionPoint(
    Electricity_208V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class Electricity_208V_60HzSystemOutletConnectionPoint(
    Electricity_208V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# === 120V_240V 60Hz
# Often the output of a transformer feeding a distribution panel
# Includes 2 x 120VAC 60Hz line, a neutral and a ground
# Used together, 2 x 120VAC = 240VAC
# Each phase can be used to provide 120VAC


class Electricity_120V_240V_60HzConnection(Connection):
    hasMedium = Electricity.AC120V_240V_60Hz
    _class_iri = None


class Electricity_120V_240V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC120V_240V_60Hz
    _class_iri = None


class Electricity_120V_240V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_120V_240V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_120V_240V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_120V_240V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_120V_240V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC120V_240V_60Hz
    _class_iri = None


class lectricity_120V_240V_60HzSystemInletConnectionPoint(
    Electricity_120V_240V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class lectricity_120V_240V_60HzSystemOutletConnectionPoint(
    Electricity_120V_240V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# === 240V 60Hz


class Electricity_240V_60HzConnection(Connection):
    hasMedium = Electricity.AC240V_60Hz
    _class_iri = None


class Electricity_240V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC240V_60Hz
    _class_iri = None


class Electricity_240V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_240V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_240V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_240V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_240V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC240V_60Hz
    _class_iri = None


class Electricity_240V_60HzSystemInletConnectionPoint(
    Electricity_240V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class Electricity_240V_60HzSystemOutletConnectionPoint(
    Electricity_240V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# === 120V 60Hz


class Electricity_120V_60HzConnection(Connection):
    hasMedium = Electricity.AC120V_60Hz
    _class_iri = None


class Electricity_120V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC120V_60Hz
    _class_iri = None


class Electricity_120V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_120V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_120V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_120V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_120V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC120V_60Hz
    _class_iri = None


class Electricity_120V_60HzSystemInletConnectionPoint(
    Electricity_120V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class Electricity_120V_60HzSystemOutletConnectionPoint(
    Electricity_120V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# === 24V 60Hz


class Electricity_24V_60HzConnection(Connection):
    hasMedium = Electricity.AC24V_60Hz
    _class_iri = None


class Electricity_24V_60HzConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.AC24V_60Hz
    _class_iri = None


class Electricity_24V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_24V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_24V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_24V_60HzConnectionPoint
):
    _class_iri = None


class Electricity_24V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.AC24V_60Hz
    _class_iri = None


class Electricity_24V_60HzSystemInletConnectionPoint(
    Electricity_24V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class Electricity_24V_60HzSystemOutletConnectionPoint(
    Electricity_24V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


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
    _class_iri = None


class OnOffSignalConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.OnOffSignal
    _class_iri = None


class OnOffSignalInletConnectionPoint(InletConnectionPoint, OnOffSignalConnectionPoint):
    _class_iri = None


class OnOffSignalOutletConnectionPoint(
    OutletConnectionPoint, OnOffSignalConnectionPoint
):
    _class_iri = None


class OnOffSignalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.OnOffSignal
    _class_iri = None


class OnOffSignalSystemInletConnectionPoint(
    OnOffSignalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class OnOffSignalSystemOutletConnectionPoint(
    OnOffSignalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# This is high level and we don't know if it's using 0-10VDC, 4-20mA, etc...
# === Modulation signals
class ModulationSignalConnection(Connection):
    hasMedium = Electricity.ModulationSignal
    _class_iri = None


class ModulationSignalConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.ModulationSignal
    _class_iri = None


class ModulationSignalInletConnectionPoint(
    InletConnectionPoint, ModulationSignalConnectionPoint
):
    _class_iri = None


class ModulationSignalOutletConnectionPoint(
    OutletConnectionPoint, ModulationSignalConnectionPoint
):
    _class_iri = None


class ModulationSignalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.ModulationSignal
    _class_iri = None


class ModulationSignalSystemInletConnectionPoint(
    ModulationSignalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class ModulationSignalSystemOutletConnectionPoint(
    ModulationSignalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


# === Networks
class RS485Connection(Connection):
    hasMedium = Electricity.RS485
    _class_iri = None


class RS485ConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.RS485
    _class_iri = None


class RS485BidirectionalConnectionPoint(
    BidirectionalConnectionPoint, RS485ConnectionPoint
):
    _class_iri = None


class RS485SystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.RS485
    _class_iri = None


class RS485BidirectionalSystemConnectionPoint(
    RS485SystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    _class_iri = None


# === Networks
class EthernetConnection(Connection):
    hasMedium = Electricity.Ethernet
    _class_iri = None


class EthernetConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.Ethernet
    _class_iri = None


class EthernetBidirectionalConnectionPoint(
    BidirectionalConnectionPoint, EthernetConnectionPoint
):
    _class_iri = None


class EthernetSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.Ethernet
    _class_iri = None


class EthernetBidirectionalSystemConnectionPoint(
    EthernetSystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    _class_iri = None
