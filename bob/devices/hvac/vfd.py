from typing import Dict

from rdflib import URIRef

from bob.properties.states import OnOffCommand

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...core import ConnectionPoint, Device, Property, p223, s223
from ...properties import (
    HP,
    RPM,
    Amps,
    ElectricPowerkW,
    OnOffStatus,
    Percent,
    PowerFactor,
)
from ...signal import AnalogIn, AnalogOut

_namespace = p223

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
    run_command: OnOffCommand
    alarm_status: OnOffStatus

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
