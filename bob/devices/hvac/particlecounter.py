from typing import Any, Dict

from rdflib import URIRef

from ...core import s223, p223, enum, Device
from ...devices import composite

from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)

from ...signal import AnalogIn

from ...sensor.particle import (
    CoarseParticulateSensor,
    FineParticulateSensor,
    UltraFineParticulateSensor,
)
from ...sensor import Sensor, define_sensors

__namespace__ = p223


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


@composite
class ParticleCounter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        if not config:
            raise ValueError("Please provide configuration dict")

        self.sensors = define_sensors(config)
        if "params" in config.keys():
            kwargs = {**config["params"], **kwargs}

        super().__init__(**kwargs)
