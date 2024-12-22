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

_namespace = P223


class AirHandlingUnit(Node):
    _class_iri: URIRef = P223["System-AirHandlingUnit"]


class Boiler(Node):
    _class_iri: URIRef = P223["System-Boiler"]


class Chiller(Node):
    _class_iri: URIRef = P223["System-Chiller"]


class CoolingTower(Node):
    _class_iri: URIRef = P223["System-CoolingTower"]


class FumeHood(Node):
    _class_iri: URIRef = P223["System-FumeHood"]


class Furnace(Node):
    _class_iri: URIRef = P223["System-Furnace"]


class HeatExchanger(Node):
    _class_iri: URIRef = P223["System-HeatExchanger"]


class HeatPump(Node):
    _class_iri: URIRef = P223["System-HeatPump"]


class HotWaterHeater(Node):
    _class_iri: URIRef = P223["System-HotWaterHeater"]


class AirToAirHeatPump(HeatPump):
    _class_iri: URIRef = P223["HeatPump-AirToAirHeatPump"]


class GroundToAirHeatPump(HeatPump):
    _class_iri: URIRef = P223["HeatPump-GroundToAirHeatPump"]


class WaterToAirHeatPump(HeatPump):
    _class_iri: URIRef = P223["HeatPump-WaterToAirHeatPump"]


class WaterToWaterHeatPump(HeatPump):
    _class_iri: URIRef = P223["HeatPump-WaterToWaterHeatPump"]


class TerminalUnit(Node):
    _class_iri: URIRef = P223["System-TerminalUnit"]


class FanCoilUnit(TerminalUnit):
    _class_iri: URIRef = P223["TerminalUnitSystem-FanCoilUnit"]


class FanPoweredTerminal(TerminalUnit):
    _class_iri: URIRef = P223["TerminalUnitSystem-FanPoweredTerminal"]


class SingleDuctTerminal(TerminalUnit):
    _class_iri: URIRef = P223["TerminalUnitSystem-SingleDuctTerminal"]


class DualDuctTerminal(TerminalUnit):
    _class_iri: URIRef = P223["TerminalUnitSystem-DualDuctTerminal"]


class ElectricalDistribution(Node):
    _class_iri: URIRef = P223["System-ElectricalDistribution"]


class ElectricalPanel(ElectricalDistribution):
    _class_iri: URIRef = P223["ElectricalDistribution-ElectricalPanel"]
