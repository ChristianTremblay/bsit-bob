from bob.properties.states import OnOffStatus
from bob.systems.functionblock import FunctionBlock
from bob.connections.occupancy import *
from bob.core import Node, PropertyReference, p223
import lighting_spaces as ls
import lighting_devices as ld
import occupancy_spaces as os

# Occupancies are shared between space... let's build a function block to relate them
class OccupancyControl(FunctionBlock):
    node_type = p223.OccupancyControl
    occupancySensor: OccupancyInletSystemConnectionPoint
    occupancyOutlet1: OccupancyOutletSystemConnectionPoint
    occupancyOutlet2: OccupancyOutletSystemConnectionPoint
    hasOccupancyStatus: PropertyReference


open_office_occ_control = OccupancyControl(
    label="OpenOffice Occ Control",
    comment="Occupancy sensor drives LightingZone1 and LightingZone2",
)
open_office_occ_control >> os.openoffice_occ_zone
open_office_occ_control.occupancySensor.mapsTo = ld.openofficeEast_movement
open_office_occ_control.occupancyOutlet1.mapsTo = ls.lighting_zone_1
open_office_occ_control.occupancyOutlet2.mapsTo = ls.lighting_zone_2
open_office_occ_control.hasOccupancyStatus = OnOffStatus(hasValue=1)
kitchenette_occ_control = OccupancyControl(
    label="Kitchenette Occ Control",
    comment="Deal with OccupancySpace6...probably not required but it's defined",
)
kitchenette_occ_control >> os.kitchenette_occ_zone
kitchenette_occ_control.occupancySensor.mapsTo = ld.kitchenette_movement
kitchenette_occ_control.occupancyOutlet1.mapsTo = ls.lighting_zone_6
kitchenette_occ_control.hasOccupancyStatus = OnOffStatus(hasValue=0)
private_office_occ_control = OccupancyControl(
    label="Private Office Occ Control",
    comment="Deal with OccupancySpace3...probably not required but it's defined",
)
private_office_occ_control.occupancySensor.mapsTo = ld.privateoffice_movement
private_office_occ_control.occupancyOutlet1.mapsTo = ls.lighting_zone_4
