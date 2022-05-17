import logging
from typing import Any, Dict

from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import Device, PropertyReference, enum, p223, quantitykind, s223, unit
from ...property import QuantifiableObservableProperty
from ...sensor import Sensor
from ...sensor.gas import (
    CH4Sensor,
    CO2Sensor,
    COSensor,
    GasConcentrationSensor,
    NO2Sensor,
)

_namespace = p223

gasmonitor_template = {
    "params": {
        "label": "Name Of Device",
        "comment": "Description",
    },
    "sensors": {
        ("label_of_sensor_1", COSensor): {
            "hasExternalReference": "bacnet://",
            #             "properties": {
            #                 ("hasMinRange", QuantifiableObservableProperty): {
            #                     "hasQuantityKind": quantitykind.DimensionlessRatio,
            #                     "unit": unit.PPM,
            #                 },
            #                 ("hasMaxRange", QuantifiableObservableProperty): {
            #                     "hasQuantityKind": quantitykind.DimensionlessRatio,
            #                     "unit": unit.PPM,
            #                 },
            #             },
        },
        ("label_of_sensor_2", NO2Sensor): {
            "hasExternalReference": "bacnet://",
            #             "hasMinRange": QuantifiableObservableProperty(
            #                 0, hasQuantityKind=quantitykind.DimensionlessRatio, unit=unit.PPM
            #             ),
            #             "hasMaxRange": QuantifiableObservableProperty(
            #                 100, hasQuantityKind=quantitykind.DimensionlessRatio, unit=unit.PPM
            #             ),
        },
    },
    "properties": {},
}


class GasMonitor(Device):
    """
    This allow the creation of a gas monitor that
    can contain 1 or more gas sensor

    to create

    monitor = GasMonitor()

    """

    node_type: URIRef = p223.GasMonitor
    airInletSupply: AirInletConnectionPoint

    alarmStatus: PropertyReference

    def __init__(self, config: Dict = gasmonitor_template, **kwargs):
        config["properties"] = config.get(
            "properties", gasmonitor_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
