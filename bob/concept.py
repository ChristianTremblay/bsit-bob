from rdflib import Graph, URIRef

from .core import (
    BOB,
    G36,
    P223,
    QUANTITYKIND,
    QUDT,
    S223,
    UNIT,
    Constituent,
    Domain,
    EnumerationKind,
    Medium,
    Mix,
    Node,
    Role,
    Substance,
)

_namespace = S223


class AirHandlingUnit(Node):
    _class_iri: URIRef = S223["System-AirHandlingUnit"]


class Boiler(Node):
    _class_iri: URIRef = S223["System-Boiler"]


class Chiller(Node):
    _class_iri: URIRef = S223["System-Chiller"]


class CoolingTower(Node):
    _class_iri: URIRef = S223["System-CoolingTower"]


class FumeHood(Node):
    _class_iri: URIRef = S223["System-FumeHood"]


class Furnace(Node):
    _class_iri: URIRef = S223["System-Furnace"]


class HeatExchanger(Node):
    _class_iri: URIRef = S223["System-HeatExchanger"]


class HeatPump(Node):
    _class_iri: URIRef = S223["System-HeatPump"]


class HotWaterHeater(Node):
    _class_iri: URIRef = S223["System-HotWaterHeater"]


class AirToAirHeatPump(HeatPump):
    _class_iri: URIRef = S223["HeatPump-AirToAirHeatPump"]


class GroundToAirHeatPump(HeatPump):
    _class_iri: URIRef = S223["HeatPump-GroundToAirHeatPump"]


class WaterToAirHeatPump(HeatPump):
    _class_iri: URIRef = S223["HeatPump-WaterToAirHeatPump"]


class WaterToWaterHeatPump(HeatPump):
    _class_iri: URIRef = S223["HeatPump-WaterToWaterHeatPump"]


class TerminalUnit(Node):
    _class_iri: URIRef = S223["System-TerminalUnit"]


class FanCoilUnit(TerminalUnit):
    _class_iri: URIRef = S223["TerminalUnit-FanCoilUnit"]


class FanPoweredTerminal(TerminalUnit):
    _class_iri: URIRef = S223["TerminalUnit-FanPoweredTerminal"]


class SingleDuctTerminal(TerminalUnit):
    _class_iri: URIRef = S223["TerminalUnit-SingleDuctTerminal"]


class DualDuctTerminal(TerminalUnit):
    _class_iri: URIRef = S223["TerminalUnit-DualDuctTerminal"]


class ElectricalDistribution(Node):
    _class_iri: URIRef = S223["System-ElectricalDistribution"]


class ElectricalPanel(ElectricalDistribution):
    _class_iri: URIRef = S223["ElectricalDistribution-ElectricalPanel"]
