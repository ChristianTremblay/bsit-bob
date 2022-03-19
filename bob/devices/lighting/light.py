from typing import Any, Dict

from rdflib import URIRef

from ...core import s223, p223, enum, Device, quantitykind, unit
from ...property import QuantifiableObservableProperty

from ...connections.light import (
    LightInletConnectionPoint,
    LightOutletConnectionPoint,
    LightVisibleOutletConnectionPoint,
)
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    Electricity_120V_60HzInletConnectionPoint,
)


from ...sensor.movement import (
    MovementSensor,
)
from ...sensor import Sensor, define_sensors

__namespace__ = p223


class Luminaire(Device):
    node_type: URIRef = p223.Light
    lightOutlet: LightVisibleOutletConnectionPoint
    electricalInlet: Electricity_120V_60HzInletConnectionPoint
