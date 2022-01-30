from typing import Any, Dict

from rdflib import URIRef

from ...core import s223, enum, Device


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

__namespace__ = s223


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


class ParticleCounter(Device):
    """"""

    node_type: URIRef = s223.ParticleCounter
    # Air inlet will allow air to enter the device
    airInletSupply: AirInletConnectionPoint
    hasSubstance: URIRef = enum["Medium-Air"]

    def __init__(self, config: Dict = None, **kwargs):
        if not config:
            raise ValueError("Please provide configuration dict")

        sensors = define_sensors(config["sensors"])
        if "device" in config.keys():
            kwargs = {**config["device"], **kwargs}

        super().__init__(**kwargs)
        for sensor in sensors:
            self > sensor
