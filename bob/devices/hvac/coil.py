from typing import Any

from ...core import s223, Device, enum


from ...connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
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

from rdflib import URIRef
from ...signal import AnalogIn

__namespace__ = s223

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


class ChilledWaterCoil(Device):
    node_type: URIRef = s223.CoolingCoil
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint


class HotWaterCoil(Device):
    node_type: URIRef = s223.HeatingCoil
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint


# Electrical Coil
class ElectricalHeatingCoil(Device):
    node_type: URIRef = s223.HeatingCoil
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    electricalInlet: ElectricalInletConnectionPoint  # can come from a SCR or a contactor...(maybe more than 1 contactor that would give x% of power)
