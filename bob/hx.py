from typing import Any

from rdflib import URIRef
from .core import (
    s223,
    Substance,
    Connection,
    ConnectionPoint,
    InletConnectionPoint,
    OutletConnectionPoint,
    SystemConnectionPoint,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    ZoneConnectionPoint,
    InletZoneConnectionPoint,
    OutletZoneConnectionPoint,
    System,
)
from .hvac import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
)

__namespace__ = s223


class PrimaryAir(System):
    pin: AirInletConnectionPoint
    pout: AirOutletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class SecondaryHotWater(System):
    sin: HotWaterInletConnectionPoint
    sout: HotWaterOutletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class HotWaterCoil(PrimaryAir, SecondaryHotWater, System):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.ain = self._connection_points["ain"] = self.pin
        self.aout = self._connection_points["aout"] = self.pout
        self.hws = self._connection_points["hws"] = self.sin
        self.hwr = self._connection_points["hwr"] = self.sout
