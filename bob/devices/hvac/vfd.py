from rdflib import URIRef
from typing import Dict
from ...core import ConnectionPoint, s223, p223, Device, Property

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...signal import AnalogIn, AnalogOut
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
    "devices": {},
}
"""


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

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        _electricalInlet = kwargs.pop("electricalInlet")
        _electricalOutlet = kwargs.pop("electricalOutlet")

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )
