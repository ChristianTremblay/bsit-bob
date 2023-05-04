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


# === Networks
class RS485Connection(Connection):
    hasMedium = Electricity.RS485
    _class_iri = S223.Connection


class RS485ConnectionPoint(ConnectionPoint):
    _attr_uriref = {"hasProtocol": P223.hasProtocol}

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
    _class_iri = BOB.BidirectionalSystemConnectionPoint


# === Networks
class EthernetConnection(Connection):
    hasMedium = Electricity.Ethernet
    _class_iri = S223.Connection


class EthernetConnectionPoint(ConnectionPoint):
    _attr_uriref = {
        "hasProtocol": P223.hasProtocol,
        "data_rate": P223.data_rate,
        "vlan": P223.VLAN,
    }
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
    _class_iri = BOB.BidirectionalSystemConnectionPoint
