import logging
from typing import Any, Dict

from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import Device, enum, p223, quantitykind, s223, unit
from ...property import QuantifiableObservableProperty
from ...sensor import Sensor
from ...sensor.gas import (
    CH4Sensor,
    CO2Sensor,
    COSensor,
    GasConcentrationSensor,
    NO2Sensor,
)
from ...signal import AnalogIn

_namespace = p223

"""
gasmonitor_template = {
    "params": {
        "label": "Name Of Device",
        "comment": "Description",
        # "hasMeasurementLocation": Connection,
    },
    "sensors": {
        ("label_of_sensor_1", COSensor): {
            "hasExternalReference": "bacnet://",
            "hasMinRange": QuantifiableObservableProperty(
                0, hasQuantityKind=quantitykind.DimensionlessRatio, unit=unit.PPM
            ),
            "hasMaxRange": QuantifiableObservableProperty(
                2000, hasQuantityKind=quantitykind.DimensionlessRatio, unit=unit.PPM
            ),
        },
        ("label_of_sensor_2", NO2Sensor): {
            "hasExternalReference": "bacnet://",
            "hasMinRange": QuantifiableObservableProperty(
                0, hasQuantityKind=quantitykind.DimensionlessRatio, unit=unit.PPM
            ),
            "hasMaxRange": QuantifiableObservableProperty(
                100, hasQuantityKind=quantitykind.DimensionlessRatio, unit=unit.PPM
            ),
        },
        # other properties could go there... ?
    },
}
"""


class GasMonitor(Device):
    """
    This allow the creation of a gas monitor that
    can contain 1 or more gas sensor

    to create

    monitor = GasMonitor()

    """

    _class_iri: URIRef = p223.GasMonitor
    airInletSupply: AirInletConnectionPoint

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        logging.debug("__init__ %r %r", config, kwargs)

        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
