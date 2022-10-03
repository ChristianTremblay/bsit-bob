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
from ...core import BOB, P223, S223, Device

_namespace = BOB


class SteamPipe(Device):
    # One way of providing humidity to air
    # a simple pie with steam
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    steamInlet: SteamInletConnectionPoint  # from the humidifier


class Humidifier(Device):
    _class_iri = P223.Humidifier
    steamOutlet: SteamOutletConnectionPoint
    waterInlet: WaterInletConnectionPoint


class ElectricalHumidifier(Humidifier):
    _class_iri = P223.Humidifier
    powerInlet: ElectricalInletConnectionPoint
    modulation = PercentCommand


class NaturalGasHumidifier(Humidifier):
    _class_iri = P223.Humidifier
    naturalGasInlet: NaturalGasInletConnectionPoint
    modulation = PercentCommand
