from typing import Any

from ...core import s223, Device, p223


from ...connections.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirBidirectionalConnectionPoint,
    CompressedAirInletConnectionPoint,
    AirConnection,
)

from ...connections.water import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
)

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)

from .damper import PneumaticDamper

from rdflib import URIRef
from ...signal import AnalogIn

__namespace__ = s223

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
    node_type: URIRef = s223.HeatExchanger
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


class Accumulator(Device):
    """
    Type of heat exchanger that accumulate heat from exhaust air
    passing through it. Then air flow will switch side. Air will flow
    so outdoor air will use energy accumulated in the substrat. This cycle
    will repeat.
    """

    node_type: URIRef = s223.HeatExchanger
    outdoorSide: AirBidirectionalConnectionPoint
    indoorSide: AirBidirectionalConnectionPoint


class Accumulator4SidesDuct(Device):
    """
    This is part of the exchanger and allow air to comes in or out of accumulator
    depending on the position of the pneumatic damper
    Return and supply are directional, but accumulator 1 and 2 are bidirectional
    """

    node_type: URIRef = p223.FourSideDuctForHeatExchanger
    accumulator1Connection: AirBidirectionalConnectionPoint
    accumulator2Connection: AirBidirectionalConnectionPoint
    supplyDuctOutlet: AirOutletConnectionPoint
    returnDuctInlet: AirInletConnectionPoint
