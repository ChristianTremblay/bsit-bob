from rdflib import URIRef
from .core import (
    s223,
    Connection,
    ConnectionPoint,
    Device,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    InletZoneConnectionPoint,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    OutletZoneConnectionPoint,
    DomainSpace,
    Substance,
    SystemConnectionPoint,
    Zone,
    ZoneConnectionPoint,
)
from .signal import AnalogIn, AnalogOut

__namespace__ = s223


Air = Substance(node_iri=s223.Air)


class AirConnection(Connection):
    hasSubstance = Air
    node_type = None


class AirConnectionPoint(ConnectionPoint):
    hasSubstance = Air
    node_type = None


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    node_type = None


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    node_type = None


class AirSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance = Air
    node_type = None


class AirInletSystemConnectionPoint(
    AirSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class AirOutletSystemConnectionPoint(
    AirSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


class AirZoneConnectionPoint(ZoneConnectionPoint):
    hasSubstance = Air
    node_type = None


class AirInletZoneConnectionPoint(AirZoneConnectionPoint, InletZoneConnectionPoint):
    node_type = None


class AirOutletZoneConnectionPoint(AirZoneConnectionPoint, OutletZoneConnectionPoint):
    node_type = None


class Fan(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


class Damper(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position: AnalogOut

    def __init__(self, label: str) -> None:
        super().__init__(label=label, position=AnalogOut(label=label + ".position"))


class Filter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    dp: AnalogIn

    def __init__(self, label: str) -> None:
        super().__init__(label=label, dp=AnalogIn(label=label + ".dp"))


class AirFlowStation(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flow: AnalogIn

    def __init__(self, label: str) -> None:
        super().__init__(label=label, flow=AnalogIn(label=label + ".flow"))


class HVACZone(Zone):
    """
    A simple HVAC Zone with a single space, and supply and return air
    connection points.
    """

    supplyAir: AirInletZoneConnectionPoint
    returnAir: AirOutletZoneConnectionPoint

    def __init__(self, label: str) -> None:
        super().__init__(label=label)

        # there is a space that is the destination of the air
        space = DomainSpace(label=label + ".space")
        space_supply_air = AirInletConnectionPoint(
            space, label=label + ".space.supplyAir"
        )
        space_return_air = AirOutletConnectionPoint(
            space, label=label + ".space.returnAir"
        )

        # map the zone connection points to the space
        self.supplyAir.maps_to(space_supply_air)
        self.returnAir.maps_to(space_return_air)
