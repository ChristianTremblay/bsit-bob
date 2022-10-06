import logging
from typing import Any, Dict

from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import BOB, P223, QUANTITYKIND, S223, UNIT, Equipment, PropertyReference, enum
from ...property import QuantifiableObservableProperty
from ...sensor import Sensor
from ...sensor.gas import (
    CH4Sensor,
    CO2Sensor,
    COSensor,
    GasConcentrationSensor,
    NO2Sensor,
)

_namespace = BOB

gasmonitor_template = {
    "params": {
        "label": "Name Of Equipment",
        "comment": "Description",
    },
    "sensors": {
        ("label_of_sensor_1", COSensor): {
            "hasExternalReference": "bacnet://",
            #             "properties": {
            #                 ("hasMinRange", QuantifiableObservableProperty): {
            #                     "hasQuantityKind": QUANTITYKIND.DimensionlessRatio,
            #                     "unit": UNIT.PPM,
            #                 },
            #                 ("hasMaxRange", QuantifiableObservableProperty): {
            #                     "hasQuantityKind": QUANTITYKIND.DimensionlessRatio,
            #                     "unit": UNIT.PPM,
            #                 },
            #             },
        },
        ("label_of_sensor_2", NO2Sensor): {
            "hasExternalReference": "bacnet://",
            #             "hasMinRange": QuantifiableObservableProperty(
            #                 0, hasQuantityKind=QUANTITYKIND.DimensionlessRatio, unit=UNIT.PPM
            #             ),
            #             "hasMaxRange": QuantifiableObservableProperty(
            #                 100, hasQuantityKind=QUANTITYKIND.DimensionlessRatio, unit=UNIT.PPM
            #             ),
        },
    },
    "properties": {},
}


class GasMonitor(Equipment):
    """
    This allow the creation of a gas monitor that
    can contain 1 or more gas sensor

    to create

    monitor = GasMonitor()

    """

    _class_iri: URIRef = P223.GasMonitor
    airInletSupply: AirInletConnectionPoint

    alarmStatus: PropertyReference

    def __init__(self, config: Dict = gasmonitor_template, **kwargs):
        config["properties"] = config.get(
            "properties", gasmonitor_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
