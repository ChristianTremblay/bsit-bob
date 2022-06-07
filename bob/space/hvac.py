from rdflib import URIRef

from bob.connections.air import (
    AirBidirectionalConnectionPoint,
    AirConnection,
    AirInletConnectionPoint,
    AirInletZoneConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletZoneConnectionPoint,
)
from bob.properties import (
    Air_Change_Per_Hour,
    GasConcentration,
    OccupancyStatus,
    RelativeHumidity,
    Temperature,
    temperature,
)
from bob.property import Setpoint

from ..core import Air, Domain, DomainSpace, Medium, Zone, enum, s223
from ..systems.physic import IndoorAir

_namespace = s223


class HVACSpace(DomainSpace):
    hasDomain = Domain.HVAC
    hasMedium: Medium = Air
    # Connection points
    ductAirInlet: AirInletConnectionPoint
    ductAirOutlet: AirOutletConnectionPoint
    airTransfer: AirBidirectionalConnectionPoint
    doors: AirBidirectionalConnectionPoint
    windows: AirBidirectionalConnectionPoint
    radiantHeating: AirBidirectionalConnectionPoint
    radiantCooling: AirBidirectionalConnectionPoint

    # Function Block
    # indoorAir: IndoorAir

    # Properties
    occupancy: OccupancyStatus
    temperature: Temperature
    humidity: RelativeHumidity
    co2: GasConcentration
    co: GasConcentration
    no2: GasConcentration
    air_change_per_hour: Air_Change_Per_Hour


class HVACZone(Zone):
    hasDomain = Domain.HVAC

    # Connection points
    airInlet: AirInletZoneConnectionPoint
    airOutlet: AirOutletZoneConnectionPoint

    # Properties
    occupancy: OccupancyStatus
    temperature: Temperature
    temperature_setpoint: Setpoint
    co2: GasConcentration
