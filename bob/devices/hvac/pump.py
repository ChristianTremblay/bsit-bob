from typing import Dict

from rdflib import URIRef

from ...connections.electricity import ElectricalInletConnectionPoint
from ...connections.water import WaterInletConnectionPoint, WaterOutletConnectionPoint
from ...core import Device, PropertyReference, s223
from ...properties import HP, RPM, Amps, ElectricPowerkW, OnOffStatus, PowerFactor

_namespace = s223

"""
fan_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "devices": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
}
"""


class Pump(Device):
    node_type: URIRef = s223.Fan
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint
    # electricalInlet: ElectricalInletConnectionPoint  # can come from a VFD
    # Properties
    amps: Amps
    rpm: RPM
    hp: HP
    kW: ElectricPowerkW
    powerFactor: PowerFactor
    hasOnOffStatus: PropertyReference
    hasOnOffCommand: PropertyReference

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        _electricalInlet = kwargs.pop("electricalInlet", None)

        super().__init__(config, **kwargs)

        if _electricalInlet:
            self.electricalInlet = _electricalInlet(
                self, label=f"{self.label}.electricalInlet"
            )
