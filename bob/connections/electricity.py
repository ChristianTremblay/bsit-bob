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
from ..signal import AnalogIn, AnalogOut

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

Electricity_575V_60Hz = Electricity("575V_60Hz")


class Electricity_575V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_575V_60Hz
    _class_iri = None


class Electricity_575V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_575V_60Hz
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
    hasMedium: Medium = Electricity_575V_60Hz
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

Electricity_480V_60Hz = Electricity("480V_60Hz")


class Electricity_480V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_480V_60Hz
    _class_iri = None


class Electricity_480V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_480V_60Hz
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
    hasMedium: Medium = Electricity_480V_60Hz
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

Electricity_347V_60Hz = Electricity("347V_60Hz")


class Electricity_347V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_347V_60Hz
    _class_iri = None


class Electricity_347V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_347V_60Hz
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
    hasMedium: Medium = Electricity_347V_60Hz
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

Electricity_277V_60Hz = Electricity("277V_60Hz")


class Electricity_277V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_277V_60Hz
    _class_iri = None


class Electricity_277V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_277V_60Hz
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
    hasMedium: Medium = Electricity_277V_60Hz
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

Electricity_208V_60Hz = Electricity("208V_60Hz")


class Electricity_208V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_208V_60Hz
    _class_iri = None


class Electricity_208V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_208V_60Hz
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
    hasMedium: Medium = Electricity_208V_60Hz
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


Electricity_120V_240V_60Hz = Electricity("120V_240V_60Hz")


class Electricity_120V_240V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_120V_240V_60Hz
    _class_iri = None


class Electricity_120V_240V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_120V_240V_60Hz
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
    hasMedium: Medium = Electricity_120V_240V_60Hz
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


Electricity_240V_60Hz = Electricity("240V_60Hz")


class Electricity_240V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_240V_60Hz
    _class_iri = None


class Electricity_240V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_240V_60Hz
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
    hasMedium: Medium = Electricity_240V_60Hz
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


Electricity_120V_60Hz = Electricity("120V_60Hz")


class Electricity_120V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_120V_60Hz
    _class_iri = None


class Electricity_120V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_120V_60Hz
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
    hasMedium: Medium = Electricity_120V_60Hz
    _class_iri = None


class Electricity_120V_60HzSystemInletConnectionPoint(
    Electricity_120V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class Electricity_120V_60HzSystemOutletConnectionPoint(
    Electricity_120V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
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


Electricity_OnOffSignal = Electricity("OnOffSignal")
# This is high level and we don't know if it's using 120V or 24VAC or 5VDC...
# It is modeling dry contact, Triac and other On-Off relationships

# === GENERAL
class OnOffSignalConnection(Connection):
    hasMedium: Medium = Electricity_OnOffSignal
    _class_iri = None


class OnOffSignalConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_OnOffSignal
    _class_iri = None


class OnOffSignalInletConnectionPoint(InletConnectionPoint, OnOffSignalConnectionPoint):
    _class_iri = None


class OnOffSignalOutletConnectionPoint(
    OutletConnectionPoint, OnOffSignalConnectionPoint
):
    _class_iri = None


class OnOffSignalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_OnOffSignal
    _class_iri = None


class OnOffSignalSystemInletConnectionPoint(
    OnOffSignalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class OnOffSignalSystemOutletConnectionPoint(
    OnOffSignalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


Electricity_ModulationSignal = Electricity("ModulationSignal")
# This is high level and we don't know if it's using 0-10VDC, 4-20mA, etc...
# === Modulation signals
class ModulationSignalConnection(Connection):
    hasMedium: Medium = Electricity_ModulationSignal
    _class_iri = None


class ModulationSignalConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_ModulationSignal
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
    hasMedium: Medium = Electricity_ModulationSignal
    _class_iri = None


class ModulationSignalSystemInletConnectionPoint(
    ModulationSignalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = None


class ModulationSignalSystemOutletConnectionPoint(
    ModulationSignalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = None


Electricity_RS485 = Electricity("RS485")
# === Networks
class RS485Connection(Connection):
    hasMedium: Medium = Electricity_RS485
    _class_iri = None


class RS485ConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_RS485
    _class_iri = None


class RS485BidirectionalConnectionPoint(
    BidirectionalConnectionPoint, RS485ConnectionPoint
):
    _class_iri = None


class RS485SystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_RS485
    _class_iri = None


class RS485BidirectionalSystemConnectionPoint(
    RS485SystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    _class_iri = None


Electricity_Ethernet = Electricity("Ethernet")
# === Networks
class EthernetConnection(Connection):
    hasMedium: Medium = Electricity_Ethernet
    _class_iri = None


class EthernetConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_Ethernet
    _class_iri = None


class EthernetBidirectionalConnectionPoint(
    BidirectionalConnectionPoint, EthernetConnectionPoint
):
    _class_iri = None


class EthernetSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_Ethernet
    _class_iri = None


class EthernetBidirectionalSystemConnectionPoint(
    EthernetSystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    _class_iri = None
