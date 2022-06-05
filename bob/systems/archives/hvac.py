from ...connections.air import (
    AirInletConnectionPoint,
    AirInletZoneConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletZoneConnectionPoint,
)
from ...core import HVAC, Domain, DomainSpace, Zone, s223

_namespace = s223


class HVACZone(Zone):
    """
    An HVAC Zone with and supply and return air connection points.
    """

    hasDomain = HVAC
    supplyAir: AirInletZoneConnectionPoint
    returnAir: AirOutletZoneConnectionPoint


class HVACZone1(HVACZone):
    """
    HVAC Zone Type 1

    A simple HVAC Zone with a single space.
    """

    _class_iri =None

    def __init__(self, label: str) -> None:
        super().__init__(label=label)

        # there is a space that is the destination of the air
        self.space = DomainSpace(label=label + ".space")

        self.supplyAir.mapsTo = AirInletConnectionPoint(
            self.space, label=label + ".space.supplyAir"
        )
        self.returnAir.mapsTo = AirOutletConnectionPoint(
            self.space, label=label + ".space.returnAir"
        )
