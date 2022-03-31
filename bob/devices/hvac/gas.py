from typing import Any, Dict

from rdflib import URIRef

from ...core import s223, p223, enum, Device, quantitykind, unit
from ...property import QuantifiableObservableProperty
from ...devices import composite, contains_devices_list
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

__namespace__ = p223

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


@composite
class GasMonitor(Device):
    """
    This allow the creation of a gas monitor that
    can contain 1 or more gas sensor

    to create

    monitor = GasMonitor()

    """

    node_type: URIRef = p223.GasMonitor
    airInletSupply: AirInletConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        _properties = {}
        for k, v in self.__annotations__.items():
            if k in kwargs:
                _properties[k] = kwargs.pop(k)
        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        self.sensors = define_sensors(config)
        self.devices, device_kwargs = contains_devices_list(config, **kwargs)

        super().__init__(**device_kwargs)

        for k, v in _properties.items():
            if v is not None:
                setattr(self, k, self.__annotations__[k](v))
