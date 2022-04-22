from rdflib import URIRef

from bob.connections.air import (
    AirBidirectionalConnectionPoint,
    AirConnection,
    AirInletConnectionPoint,
    AirInletZoneConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletZoneConnectionPoint,
)
from bob.properties.states import OccupancyStatus

from ..core import HVAC, Air, DomainSpace, Medium, Zone, enum, s223
from ..systems.physic import IndoorAir

_namespace = s223


class HVACSpace(DomainSpace):
    hasDomain = HVAC
    hasMedium: Medium = Air
    ductAirInlet: AirInletConnectionPoint
    ductAirOutlet: AirOutletConnectionPoint
    airTransfer: AirBidirectionalConnectionPoint
    doors: AirBidirectionalConnectionPoint
    windows: AirBidirectionalConnectionPoint
    radiantHeating: AirBidirectionalConnectionPoint
    radiantCooling: AirBidirectionalConnectionPoint
    indoorAir: IndoorAir
    occupancy: OccupancyStatus

    def __init__(self, **kwargs):
        if "indoorAir" in kwargs:
            ia = kwargs.pop("indoorAir")
        else:
            ia = IndoorAir(label="Indoor air of space")
        super().__init__(**kwargs)
        self.indoorAir = ia
        self.indoorAir.ductAirInlet.mapsTo = self.ductAirInlet
        self.indoorAir.ductAirOutlet.mapsTo = self.ductAirOutlet
        self.indoorAir.airTransfer.mapsTo = self.airTransfer
        self.indoorAir.doors.mapsTo = self.doors
        self.indoorAir.windows.mapsTo = self.windows
        self.indoorAir.radiantHeating.mapsTo = self.radiantHeating
        self.indoorAir.radiantCooling.mapsTo = self.radiantCooling


class HVACZone(Zone):
    hasDomain = HVAC
    airInlet: AirInletZoneConnectionPoint
    airOutlet: AirOutletZoneConnectionPoint
    occupancy: OccupancyStatus
