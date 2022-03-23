from typing import Any, Dict

from rdflib import URIRef
from bob.properties.electricity import ElectricPowerW

from ...properties.light import Brightness
from ...properties.ratio import Percent, PercentCommand
from ...properties.states import OnOffStatus

from ...devices import contains_devices_list

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
    node_type: URIRef = p223.Luminaire
    lightOutlet: LightVisibleOutletConnectionPoint
    brightness: Brightness
    brightnessRatio: PercentCommand
    hasOnOffStatus: OnOffStatus
    electricalPower: ElectricPowerW

    def __init__(self, config: Dict = None, **kwargs):
        optional_properties = ["brightness"]
        _properties = {}
        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        sensors = define_sensors(config)
        devices, device_kwargs = contains_devices_list(config, **kwargs)

        _electricalInlet = (
            device_kwargs.pop("electricalInlet")
            if "electricalInlet" in device_kwargs
            else None
        )

        for each in optional_properties:
            _properties[each] = (
                device_kwargs.pop(each) if each in device_kwargs else None
            )

        super().__init__(**device_kwargs)
        self.electricalInlet = (
            _electricalInlet(self, label=f"{self.label}.electricalInlet")
            if _electricalInlet
            else None
        )
        for k, v in _properties.items():
            if v:
                setattr(self, k, self.__annotations__[k](v))
        for sensor in sensors:
            self > sensor
        for dev in devices:
            self > dev
