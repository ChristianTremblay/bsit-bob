from typing import Any, Dict

from rdflib import URIRef

from ...core import s223, p223, enum, Device, quantitykind, unit, Value
from ...property import QuantifiableObservableProperty

from ...connections.light import LightInletConnectionPoint, LightOutletConnectionPoint
from ...connections.electricity import ElectricalInletConnectionPoint


from ...sensor.movement import (
    MovementSensor,
)
from ...sensor import Sensor, define_sensors

__namespace__ = p223


class Light(Device):
    node_type: URIRef = p223.Light
    lightOutlet: LightOutletConnectionPoint
    electricalInlet: ElectricalInletConnectionPoint
