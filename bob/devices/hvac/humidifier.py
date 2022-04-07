from typing import Any

from rdflib import URIRef

from bob.connections.naturalgas import NaturalGasInletConnectionPoint

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import ElectricalInletConnectionPoint
from ...connections.water import (
    SteamInletConnectionPoint,
    SteamOutletConnectionPoint,
    WaterInletConnectionPoint,
)
from ...core import Device, p223, s223
from ...signal import AnalogOut

__namespace__ = p223


class SteamPipe(Device):
    # One way of providing humidity to air
    # a simple pie with steam
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    steamInlet: SteamInletConnectionPoint  # from the humidifier


class Humidifier(Device):
    node_type: URIRef = p223.Humidifier
    steamOutlet: SteamOutletConnectionPoint
    waterInlet: WaterInletConnectionPoint


class ElectricalHumidifier(Humidifier):
    powerInlet: ElectricalInletConnectionPoint
    modulation = AnalogOut


class NaturalGasHumidifier(Humidifier):
    naturalGasInlet: NaturalGasInletConnectionPoint
    modulation = AnalogOut
