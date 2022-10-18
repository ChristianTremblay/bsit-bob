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

from ..core import BOB, P223, S223, Air, Domain, DomainSpace, Medium, Zone, enum

_namespace = BOB


class HVACSpace(DomainSpace):
    _class_iri = P223.HVACSpace
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
    _class_iri = P223.HVACZone
    hasDomain = Domain.HVAC

    # Connection points
    airInlet: AirInletZoneConnectionPoint
    airOutlet: AirOutletZoneConnectionPoint

    # Properties
    occupancy: OccupancyStatus
    temperature: Temperature
    temperature_setpoint: Setpoint
    co2: GasConcentration
