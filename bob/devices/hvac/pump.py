from rdflib import URIRef
from typing import Dict

from ...properties import Amps, ElectricPowerkW, PowerFactor, RPM, HP, OnOffStatus
from ...connections.electricity import ElectricalInletConnectionPoint
from ...core import PropertyReference, s223, Device


from ...connections.water import WaterInletConnectionPoint, WaterOutletConnectionPoint

__namespace__ = s223

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
