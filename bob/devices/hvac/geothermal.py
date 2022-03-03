from typing import Any

from ...core import p223, Device, enum


from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    AirBidirectionalConnectionPoint,
)

from ...connections.water import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
)

from rdflib import URIRef
from ...signal import AnalogIn

__namespace__ = p223

"""
chilledWaterCoil_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "contains": {("valve", Device): {"comment": "SubDev comment"}},
}
"""
# SEMANTIC QUESTION
# here, that could be a good way to define the coil and its valve...
# but the valve connect to the coil
# can this be considered "contained" in the Coil device ?
# Should this b ea system


class GeothermalWell(Device):
    node_type: URIRef = p223.GeothermalWell
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint
