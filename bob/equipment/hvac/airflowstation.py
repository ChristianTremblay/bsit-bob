from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...core import BOB, S223, Equipment, P223
from ...sensor.flow import AirFlowSensor

_namespace = BOB


class AirFlowMonitor(Equipment):
    _class_iri = P223.AirFlowMonitor
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flowSensor: AirFlowSensor


# TODO : Create the template and make that the same than the others.
