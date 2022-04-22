from typing import Any, Dict

from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import Device, enum, p223, s223
from ...sensor import Sensor
from ...sensor.particle import (
    CoarseParticulateSensor,
    FineParticulateSensor,
    UltraFineParticulateSensor,
)
from ...signal import AnalogIn

_namespace = p223


"""
particlecounter_template = {
    "sensors": {
        ("label_of_sensor_1", CoarseParticulateSensor): {
            "hasExternalReference": "bacnet://",
            "comment": "Coarse Particles 10.0um or less",
        },
        ("label_of_sensor_2", FineParticulateSensor): {
            "hasExternalReference": "bacnet://",
            "comment": "Fine Particles 2.5um or less",
        },
        ("label_of_sensor_3", UltraFineParticulateSensor): {
            "hasExternalReference": "bacnet://",
            "comment": "Ultra Fine Particles 1.0um or less",
        },
    }
}
"""


class ParticleCounter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
