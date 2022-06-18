from typing import Any

from rdflib import URIRef

from bob.connections.naturalgas import NaturalGasInletConnectionPoint
from bob.properties import Percent, PercentCommand

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import ElectricalInletConnectionPoint
from ...connections.water import (
    SteamInletConnectionPoint,
    SteamOutletConnectionPoint,
    WaterInletConnectionPoint,
)
from ...core import Device, bob, p223, s223

_namespace = bob


class SteamPipe(Device):
    # One way of providing humidity to air
    # a simple pie with steam
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    steamInlet: SteamInletConnectionPoint  # from the humidifier


class Humidifier(Device):
    _class_iri = p223.Humidifier
    steamOutlet: SteamOutletConnectionPoint
    waterInlet: WaterInletConnectionPoint


class ElectricalHumidifier(Humidifier):
    _class_iri = p223.Humidifier
    powerInlet: ElectricalInletConnectionPoint
    modulation = PercentCommand


class NaturalGasHumidifier(Humidifier):
    _class_iri = p223.Humidifier
    naturalGasInlet: NaturalGasInletConnectionPoint
    modulation = PercentCommand
