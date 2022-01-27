from rdflib import URIRef
from ...core import s223, Device

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...signal import AnalogIn, AnalogOut


from ...sensor import Sensor

__namespace__ = s223


class AirFlowStation(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flow = AnalogIn
    flowSensor: Sensor
