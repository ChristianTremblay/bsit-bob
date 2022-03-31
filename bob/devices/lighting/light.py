from typing import Any, Dict

from rdflib import URIRef
from bob.properties.electricity import ElectricPowerW

from ...properties.light import Brightness, RelativeLuminousFlux
from ...properties.ratio import Percent, PercentCommand
from ...properties.states import OnOffStatus

from ...devices import composite, contains_devices_list

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


@composite
class Luminaire(Device):
    node_type: URIRef = p223.Luminaire
    lightOutlet: LightVisibleOutletConnectionPoint
    brightness: RelativeLuminousFlux
    brightnessRatio: PercentCommand
    hasOnOffStatus: OnOffStatus
    electricalPower: ElectricPowerW

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

        _electricalInlet = device_kwargs.pop("electricalInlet", None)

        super().__init__(**device_kwargs)
        self.electricalInlet = (
            _electricalInlet(self, label=f"{self.label}.electricalInlet")
            if _electricalInlet
            else None
        )
        for k, v in _properties.items():
            if v is not None:
                setattr(self, k, self.__annotations__[k](v))
