from typing import Any

from rdflib import URIRef

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...connections.liquid import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import BOB, P223, S223, Equipment, enum

_namespace = BOB

"""
chilledWaterCoil_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "equipment": {("valve", Equipment): {"comment": "SubDev comment"}},
}
"""
# SEMANTIC QUESTION
# here, that could be a good way to define the coil and its valve...
# but the valve connect to the coil
# can this be considered "contained" in the Coil Equipment ?
# Should this b ea system


class GeothermalWell(Equipment):
    _class_iri: URIRef = P223.GeothermalWell
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint
