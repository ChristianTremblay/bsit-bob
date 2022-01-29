from typing import Any

from rdflib import URIRef

from ...core import s223, enum, Device


from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)

from ...signal import AnalogIn

from ...sensor.particle import (
    CoarseParticulateSensor,
    FineParticulateSensor,
    UltraFineParticulateSensor,
)

__namespace__ = s223


class ParticleCounter(Device):
    node_type = s223.ParticleCounter
    # Air inlet provided as sometimes a tube is
    # connected and air is provided by a pump
    airInletSupply: AirInletConnectionPoint
    hasSubstance: URIRef = enum["Medium-Air"]

    # I probbaly need types for the extref here
    # TODO :

    def __init__(self, **kwargs):
        coarse_extref = None
        fine_extref = None
        ultrafine_extref = None
        if "coarse_extref" in kwargs:
            coarse_extref = kwargs.pop("coarse_extref")
        if "fine_extref" in kwargs:
            fine_extref = kwargs.pop("fine_extref")
        if "ultrafine_extref" in kwargs:
            ultrafine_extref = kwargs.pop("ultrafine_extref")

        super().__init__(**kwargs)

        coarseSensor = CoarseParticulateSensor(extref=coarse_extref)
        fineSensor = FineParticulateSensor(extref=fine_extref)
        ultraFineSensor = UltraFineParticulateSensor(extref=ultrafine_extref)

        self > coarseSensor
        self > fineSensor
        self > ultraFineSensor
