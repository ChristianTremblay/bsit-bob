import logging
from typing import Any, Dict

from rdflib import URIRef

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import (
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
    Equipment,
    PropertyReference,
    Substance,
    enum,
)
from ...property import QuantifiableObservableProperty
from ...sensor import Sensor
from ...sensor.gas import (
    CH4Sensor,
    CO2Sensor,
    COSensor,
    GasConcentrationSensor,
    NO2Sensor,
)

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

gasmonitor_template = {
    "params": {
        "label": "Name Of Equipment",
        "comment": "Description",
    },
    "sensors": {
        ("COSensor", COSensor): {
            "hasExternalReference": "bacnet://",
            # "properties": {
            #   "ofSubstance": Substance.CO,
            #                 ("hasMinRange", QuantifiableObservableProperty): {
            #                     "hasQuantityKind": QUANTITYKIND.DimensionlessRatio,
            #                     "hasUnit": UNIT.PPM,
            #                 },
            #                 ("hasMaxRange", QuantifiableObservableProperty): {
            #                     "hasQuantityKind": QUANTITYKIND.DimensionlessRatio,
            #                     "hasUnit": UNIT.PPM,
            #                 },
            # },
        },
        ("NO2Sensor", NO2Sensor): {
            "hasExternalReference": "bacnet://",
            # "properties": {
            # "ofSubstance": Substance.NO2,
            #             "hasMinRange": QuantifiableObservableProperty(
            #                 0, hasQuantityKind=QUANTITYKIND.DimensionlessRatio, hasUnit=UNIT.PPM
            #             ),
            #             "hasMaxRange": QuantifiableObservableProperty(
            #                 100, hasQuantityKind=QUANTITYKIND.DimensionlessRatio, hasUnit=UNIT.PPM
            #             ),
            #    },
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
