from typing import Dict


from bob.enum import ElectricalPhaseIdentifier, Aspect
from bob.properties import ElectricPowerkW
from bob.properties.electricity import Amps

from ...connections import electricity as elec_cnx
from ...core import (
    BOB,
    P223,
    S223,
    Equipment,
    System,
    QuantifiableObservableProperty,
)

_namespace = BOB


class Transformer(Equipment):
    _class_iri = S223.ElectricEnergyTransformer
    hasPower: ElectricPowerkW

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

class CircuitBreaker(Equipment):
    _class_iri = S223.ElectricBreaker
    # electricalInlet: ElectricalInletConnectionPoint
    # electricalOutlet: ElectricalOutletConnectionPoint


    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        amps = kwargs.pop("amps")

        super().__init__(config, **kwargs)

        self.currentRating = Amps(
            amps, label="Current rating of breaker", hasAspect=Aspect.Nominal
        )