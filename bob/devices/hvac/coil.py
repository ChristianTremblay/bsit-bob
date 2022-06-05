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
from ...connections.water import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import Device, s223
from ...signal import AnalogIn

_namespace = s223

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


class WaterCoil(Device):
    _class_iri: URIRef = s223.Coil
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint


class ChilledWaterCoil(Device):
    _class_iri: URIRef = s223.CoolingCoil
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint


class HotWaterCoil(Device):
    _class_iri: URIRef = s223.HeatingCoil
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint


# Electrical Coil
class ElectricalHeatingCoil(Device):
    _class_iri: URIRef = s223.HeatingCoil
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    electricalInlet: ElectricalInletConnectionPoint  # can come from a SCR or a contactor...(maybe more than 1 contactor that would give x% of power)


# Baseboard, radiant panel, heating floor
class ElectricalRadiantHeatingCoil(Device):
    _class_iri: URIRef = s223.HeatingCoil
    airContact: AirBidirectionalConnectionPoint
    electricalInlet: ElectricalInletConnectionPoint  # can come from a SCR or a contactor...(maybe more than 1 contactor that would give x% of power)
