from .sensor import Sensor
from rdflib import URIRef
from ..core import quantitykind, s223

__namespace__ = s223


class TemperatureSensor(Sensor):
    node_type: URIRef = s223.TemperatureSensor
    hasQuantityKind: URIRef = quantitykind.Temperature
