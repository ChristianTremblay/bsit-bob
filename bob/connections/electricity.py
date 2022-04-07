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

__namespace__ = s223


# === GENERAL
class ElectricalConnection(Connection):
    hasMedium: Medium = Electricity
    node_type = None


class ElectricalConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity
    node_type = None


class ElectricalInletConnectionPoint(InletConnectionPoint, ElectricalConnectionPoint):
    node_type = None


class ElectricalOutletConnectionPoint(OutletConnectionPoint, ElectricalConnectionPoint):
    node_type = None


class ElectricalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity
    node_type = None


class ElectricalSystemInletConnectionPoint(
    ElectricalSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class ElectricalSystemOutletConnectionPoint(
    ElectricalSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


# === 575V 60Hz

Electricity_575V_60Hz = Medium(node_iri=s223["Electricity-575V_60Hz"])


class Electricity_575V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_575V_60Hz
    node_type = None


class Electricity_575V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_575V_60Hz
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
    hasMedium: Medium = Electricity_575V_60Hz
    node_type = None


class Electricity_575V_60HzSystemInletConnectionPoint(
    Electricity_575V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class Electricity_575V_60HzSystemOutletConnectionPoint(
    Electricity_575V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


# === 480V 60Hz

Electricity_480V_60Hz = Medium(node_iri=s223["Electricity-480V_60Hz"])


class Electricity_480V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_480V_60Hz
    node_type = None


class Electricity_480V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_480V_60Hz
    node_type = None


class Electricity_480V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_480V_60HzConnectionPoint
):
    node_type = None


class Electricity_480V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_480V_60HzConnectionPoint
):
    node_type = None


class Electricity_480V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_480V_60Hz
    node_type = None


class Electricity_480V_60HzSystemInletConnectionPoint(
    Electricity_480V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class Electricity_480V_60HzSystemOutletConnectionPoint(
    Electricity_480V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


# === 347V 60Hz
# 1 phase of 575V

Electricity_347V_60Hz = Medium(node_iri=s223["Electricity-347V_60Hz"])


class Electricity_347V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_347V_60Hz
    node_type = None


class Electricity_347V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_347V_60Hz
    node_type = None


class Electricity_347V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_347V_60HzConnectionPoint
):
    node_type = None


class Electricity_347V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_347V_60HzConnectionPoint
):
    node_type = None


class Electricity_347V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_347V_60Hz
    node_type = None


class Electricity_347V_60HzSystemInletConnectionPoint(
    Electricity_347V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class Electricity_347V_60HzSystemOutletConnectionPoint(
    Electricity_347V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


# === 277V 60Hz
# 1 phase of 480V (US)

Electricity_277V_60Hz = Medium(node_iri=s223["Electricity-277V_60Hz"])


class Electricity_277V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_277V_60Hz
    node_type = None


class Electricity_277V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_277V_60Hz
    node_type = None


class Electricity_277V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_277V_60HzConnectionPoint
):
    node_type = None


class Electricity_277V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_277V_60HzConnectionPoint
):
    node_type = None


class Electricity_277V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_277V_60Hz
    node_type = None


class Electricity_277V_60HzSystemInletConnectionPoint(
    Electricity_277V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class Electricity_277V_60HzSystemOutletConnectionPoint(
    Electricity_277V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


# === 208V 60Hz
# 3 phase

Electricity_208V_60Hz = Medium(node_iri=s223["Electricity-208V_60Hz"])


class Electricity_208V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_208V_60Hz
    node_type = None


class Electricity_208V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_208V_60Hz
    node_type = None


class Electricity_208V_60HzInletConnectionPoint(
    InletConnectionPoint, Electricity_208V_60HzConnectionPoint
):
    node_type = None


class Electricity_208V_60HzOutletConnectionPoint(
    OutletConnectionPoint, Electricity_208V_60HzConnectionPoint
):
    node_type = None


class Electricity_208V_60HzSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_208V_60Hz
    node_type = None


class Electricity_208V_60HzSystemInletConnectionPoint(
    Electricity_208V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class Electricity_208V_60HzSystemOutletConnectionPoint(
    Electricity_208V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


# === 120V_240V 60Hz
# Often the output of a transformer feeding a distribution panel
# Includes 2 x 120VAC 60Hz line, a neutral and a ground
# Used together, 2 x 120VAC = 240VAC
# Each phase can be used to provide 120VAC


Electricity_120V_240V_60Hz = Medium(node_iri=s223["Electricity-120V_240V_60Hz"])


class Electricity_120V_240V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_120V_240V_60Hz
    node_type = None


class Electricity_120V_240V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_120V_240V_60Hz
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
    hasMedium: Medium = Electricity_120V_240V_60Hz
    node_type = None


class lectricity_120V_240V_60HzSystemInletConnectionPoint(
    Electricity_120V_240V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class lectricity_120V_240V_60HzSystemOutletConnectionPoint(
    Electricity_120V_240V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


# === 240V 60Hz


Electricity_240V_60Hz = Medium(node_iri=s223["Electricity-240V_60Hz"])


class Electricity_240V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_240V_60Hz
    node_type = None


class Electricity_240V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_240V_60Hz
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
    hasMedium: Medium = Electricity_240V_60Hz
    node_type = None


class Electricity_240V_60HzSystemInletConnectionPoint(
    Electricity_240V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class Electricity_240V_60HzSystemOutletConnectionPoint(
    Electricity_240V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


# === 120V 60Hz


Electricity_120V_60Hz = Medium(node_iri=s223["Electricity-120V_60Hz"])


class Electricity_120V_60HzConnection(Connection):
    hasMedium: Medium = Electricity_120V_60Hz
    node_type = None


class Electricity_120V_60HzConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_120V_60Hz
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
    hasMedium: Medium = Electricity_120V_60Hz
    node_type = None


class Electricity_120V_60HzSystemInletConnectionPoint(
    Electricity_120V_60HzSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class Electricity_120V_60HzSystemOutletConnectionPoint(
    Electricity_120V_60HzSystemConnectionPoint, OutletSystemConnectionPoint
):
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


Electricity_OnOffSignal = Medium(node_iri=s223["Electricity-OnOffSignal"])
# This is high level and we don't know if it's using 120V or 24VAC or 5VDC...
# It is modeling dry contact, Triac and other On-Off relationships

# === GENERAL
class OnOffSignalConnection(Connection):
    hasMedium: Medium = Electricity_OnOffSignal
    node_type = None


class OnOffSignalConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_OnOffSignal
    node_type = None


class OnOffSignalInletConnectionPoint(InletConnectionPoint, OnOffSignalConnectionPoint):
    node_type = None


class OnOffSignalOutletConnectionPoint(
    OutletConnectionPoint, OnOffSignalConnectionPoint
):
    node_type = None


class OnOffSignalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_OnOffSignal
    node_type = None


class OnOffSignalSystemInletConnectionPoint(
    OnOffSignalSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class OnOffSignalSystemOutletConnectionPoint(
    OnOffSignalSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


Electricity_ModulationSignal = Medium(node_iri=s223["Electricity-ModulationSignal"])
# This is high level and we don't know if it's using 0-10VDC, 4-20mA, etc...
# === Modulation signals
class ModulationSignalConnection(Connection):
    hasMedium: Medium = Electricity_ModulationSignal
    node_type = None


class ModulationSignalConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_ModulationSignal
    node_type = None


class ModulationSignalInletConnectionPoint(
    InletConnectionPoint, ModulationSignalConnectionPoint
):
    node_type = None


class ModulationSignalOutletConnectionPoint(
    OutletConnectionPoint, ModulationSignalConnectionPoint
):
    node_type = None


class ModulationSignalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_ModulationSignal
    node_type = None


class ModulationSignalSystemInletConnectionPoint(
    ModulationSignalSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class ModulationSignalSystemOutletConnectionPoint(
    ModulationSignalSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


Electricity_RS485 = Medium(node_iri=s223["Electricity-RS485"])
# === Networks
class RS485Connection(Connection):
    hasMedium: Medium = Electricity_RS485
    node_type = None


class RS485ConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_RS485
    node_type = None


class RS485BidirectionalConnectionPoint(
    BidirectionalConnectionPoint, RS485ConnectionPoint
):
    node_type = None


class RS485SystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_RS485
    node_type = None


class RS485BidirectionalSystemConnectionPoint(
    RS485SystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    node_type = None


Electricity_Ethernet = Medium(node_iri=s223["Electricity-Ethernet"])
# === Networks
class EthernetConnection(Connection):
    hasMedium: Medium = Electricity_Ethernet
    node_type = None


class EthernetConnectionPoint(ConnectionPoint):
    hasMedium: Medium = Electricity_Ethernet
    node_type = None


class EthernetBidirectionalConnectionPoint(
    BidirectionalConnectionPoint, EthernetConnectionPoint
):
    node_type = None


class EthernetSystemConnectionPoint(SystemConnectionPoint):
    hasMedium: Medium = Electricity_Ethernet
    node_type = None


class EthernetBidirectionalSystemConnectionPoint(
    EthernetSystemConnectionPoint, BidirectionalSystemConnectionPoint
):
    node_type = None
