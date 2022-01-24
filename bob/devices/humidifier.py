from typing import Any

from bob.connections.naturalgas import NaturalGasInletConnectionPoint

from ..core import (
    s223,
)

from ..node import Device

from ..connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)

from ..connections.water import (
    SteamOutletConnectionPoint,
    WaterInletConnectionPoint,
    SteamInletConnectionPoint,
)

from ..connections.electricity import (
    ElectricalInletConnectionPoint,
)

from ..signal import AnalogOut

__namespace__ = s223


class SteamPipe(Device):
    # One way of providing humidity to air
    # a simple pie with steam
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    steamInlet: SteamInletConnectionPoint  # from the humidifier


class Humidifier(Device):
    steamOutlet: SteamOutletConnectionPoint
    waterInlet: WaterInletConnectionPoint


class ElectricalHumidifier(Humidifier):
    powerInlet: ElectricalInletConnectionPoint
    modulation = AnalogOut


class NaturalGasHumidifier(Humidifier):
    naturalGasInlet: NaturalGasInletConnectionPoint
    modulation = AnalogOut
