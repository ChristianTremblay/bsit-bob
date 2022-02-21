from rdflib import URIRef
from ...core import s223, p223, Device

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...signal import AnalogIn, AnalogOut


from ...sensor import Sensor

__namespace__ = p223


class AirFlowMonitor(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flow = AnalogIn
    flowSensor: Sensor


# TODO : Create the template and make that the same than the others.
