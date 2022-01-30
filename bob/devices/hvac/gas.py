from typing import Any, Dict

from rdflib import URIRef

from ...core import s223, enum, Device, quantitykind, unit, Value


from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)

from ...signal import AnalogIn

from ...sensor.gas import (
    COSensor,
    CO2Sensor,
    NO2Sensor,
    CH4Sensor,
    GasConcentrationSensor,
)
from ...sensor import Sensor, define_sensors

__namespace__ = s223

gasmonitor_template = {
    "device": {
        "label": "Name Of Device",
        "comment": "Description",
        # "hasMeasurementLocation": Connection,
    },
    "sensors": {
        ("label_of_sensor_1", COSensor): {
            "hasExternalReference": "bacnet://",
            "hasMinRange": Value(
                0, hasQuantityKind=quantitykind.Concentration, unit=unit.PPM
            ),
            "hasMaxRange": Value(
                2000, hasQuantityKind=quantitykind.Concentration, unit=unit.PPM
            ),
        },
        ("label_of_sensor_2", NO2Sensor): {
            "hasExternalReference": "bacnet://",
            "hasMinRange": Value(
                0, hasQuantityKind=quantitykind.Concentration, unit=unit.PPM
            ),
            "hasMaxRange": Value(
                100, hasQuantityKind=quantitykind.Concentration, unit=unit.PPM
            ),
        },
        # other properties could go there... ?
    },
}


class GasMonitor(Device):
    """
    This allow the creation of a gas monitor that
    can contain 1 or more gas sensor

    to create

    monitor = GasMonitor()

    """

    node_type: URIRef = s223.GazMonitor
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
