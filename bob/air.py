from rdflib import URIRef
from .core import (
    s223,
    Connection,
    ConnectionPoint,
    Device,
    InletConnectionPoint,
    InletSpaceConnectionPoint,
    InletSystemConnectionPoint,
    InletZoneConnectionPoint,
    OutletConnectionPoint,
    OutletSpaceConnectionPoint,
    OutletSystemConnectionPoint,
    OutletZoneConnectionPoint,
    Space,
    SpaceConnectionPoint,
    Substance,
    SystemConnectionPoint,
    Zone,
    ZoneConnectionPoint,
)
from .signal import AnalogIn, AnalogOut

__namespace__ = s223


class Air(Substance):
    pass


class AirConnection(Connection):
    hasSubstance: URIRef = Air.node_type
    node_type = None


class AirConnectionPoint(ConnectionPoint):
    hasSubstance: URIRef = Air.node_type
    node_type = None


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    node_type = None


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    node_type = None


class AirSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance: URIRef = Air.node_type
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
    hasSubstance: URIRef = Air.node_type
    node_type = None


class AirInletZoneConnectionPoint(AirZoneConnectionPoint, InletZoneConnectionPoint):
    node_type = None


class AirOutletZoneConnectionPoint(AirZoneConnectionPoint, OutletZoneConnectionPoint):
    node_type = None


class AirSpaceConnectionPoint(SpaceConnectionPoint):
    node_type = None
    hasSubstance: URIRef = Air.node_type


class AirInletSpaceConnectionPoint(AirSpaceConnectionPoint, InletSpaceConnectionPoint):
    node_type = None
    hasDirection: URIRef = s223.Inlet


class AirOutletSpaceConnectionPoint(
    AirSpaceConnectionPoint, OutletSpaceConnectionPoint
):
    node_type = None
    hasDirection: URIRef = s223.Outlet


class Fan(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


class Damper(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position = AnalogOut


class Filter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    dp = AnalogOut


class AirFlowStation(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flow = AnalogIn


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
        space = Space(label="Space")
        space_supply_air = AirInletSpaceConnectionPoint(
            space, label=label + ".space.supplyAir"
        )
        space_return_air = AirOutletSpaceConnectionPoint(
            space, label=label + ".space.returnAir"
        )

        # map the zone connection points to the space
        self.supplyAir.maps_to(space_supply_air)
        self.returnAir.maps_to(space_return_air)
