from typing import Any

from rdflib import URIRef

from ...connections.air import (
    AirBidirectionalConnectionPoint,
    AirConnection,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    CompressedAirInletConnectionPoint,
)
from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)
from ...connections.water import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
)
from ...core import Device, BOB, P223, S223

_namespace = BOB

"""
chilledWaterCoil_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "devices": {("valve", Device): {"comment": "SubDev comment"}},
}
"""
# SEMANTIC QUESTION
# here, that could be a good way to define the coil and its valve...
# but the valve connect to the coil
# can this be considered "contained" in the Coil device ?
# Should this b ea system


class HeatExchanger(Device):
    _class_iri: URIRef = S223.HeatExchanger
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


class Accumulator(Device):
    """
    Type of heat exchanger that accumulate heat from exhaust air
    passing through it. Then air flow will switch side. Air will flow
    so outdoor air will use energy accumulated in the substrat. This cycle
    will repeat.
    """

    _class_iri: URIRef = S223.HeatExchanger
    outdoorSide: AirBidirectionalConnectionPoint
    indoorSide: AirBidirectionalConnectionPoint


class Accumulator4SidesDuct(Device):
    """
    This is part of the exchanger and allow air to comes in or out of accumulator
    depending on the position of the pneumatic damper
    Return and supply are directional, but accumulator 1 and 2 are bidirectional
    """

    _class_iri: URIRef = S223.HeatExchanger
    accumulator1Connection: AirBidirectionalConnectionPoint
    accumulator2Connection: AirBidirectionalConnectionPoint
    supplyDuctOutlet: AirOutletConnectionPoint
    returnDuctInlet: AirInletConnectionPoint
