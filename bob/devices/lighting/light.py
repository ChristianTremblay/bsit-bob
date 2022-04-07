from typing import Dict

from rdflib import URIRef

from bob.properties.electricity import ElectricPowerW

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    Electricity_120V_60HzInletConnectionPoint,
)
from ...connections.light import LightVisibleOutletConnectionPoint
from ...core import Device, s223
from ...properties.light import RelativeLuminousFlux
from ...properties.ratio import PercentCommand
from ...properties.states import OnOffStatus

__namespace__ = s223


class Luminaire(Device):
    node_type: URIRef = s223.Luminaire
    lightOutlet: LightVisibleOutletConnectionPoint
    brightness: RelativeLuminousFlux
    brightnessRatio: PercentCommand
    hasOnOffStatus: OnOffStatus
    electricalPower: ElectricPowerW

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        _electricalInlet = kwargs.pop("electricalInlet", None)

        super().__init__(config, **kwargs)

        if _electricalInlet:
            self.electricalInlet = _electricalInlet(
                self, label=f"{self.label}.electricalInlet"
            )
