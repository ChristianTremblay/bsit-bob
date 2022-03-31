from rdflib import URIRef
from typing import Dict
from ...core import ConnectionPoint, s223, p223, Device, Property

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...signal import AnalogIn, AnalogOut
from ...sensor import define_sensors
from ...devices import composite, contains_devices_list
from ...properties import (
    Amps,
    ElectricPowerkW,
    PowerFactor,
    OnOffStatus,
    HP,
    RPM,
    Percent,
)

__namespace__ = p223

"""
vfd_template = {
    "params": {
        "label": "MyVFD", 
        "comment": "A VFD for a Big Fan",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
        "amps": 10,
        "hp": 10,
    },
    "sensors": {},
    "contains": {},
}
"""


@composite
class VFD(Device):
    node_type: URIRef = s223.VariableFrequencyDrive
    # electricalInlet: Must be provided in config
    # electricalOutlet: Must be provided in config
    amps: Amps
    hp: HP
    kW: ElectricPowerkW
    speed_reference: Percent
    rpm: RPM
    # motor_temp: ?
    drive_running: OnOffStatus
    alarmStatus: OnOffStatus

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
        _electricalOutlet = device_kwargs.pop("electricalOutlet", None)

        super().__init__(**device_kwargs)
        self.electricalInlet = (
            _electricalInlet(self, label=f"{self.label}.electricalInlet")
            if _electricalInlet
            else None
        )
        self.electricalOutlet = (
            _electricalOutlet(self, label=f"{self.label}.electricalOutlet")
            if _electricalOutlet
            else None
        )
        for k, v in _properties.items():
            if v is not None:
                setattr(self, k, self.__annotations__[k](v))
