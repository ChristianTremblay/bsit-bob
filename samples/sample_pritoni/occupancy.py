from bob.properties.states import OnOffStatus
from bob.systems.occupancy.occupancy import OccupancyControl
from bob.connections.occupancy import *
from bob.core import Node, PropertyReference, p223
from bob.properties.states import OccupancyStatus
import lighting_spaces as ls
import lighting_devices as ld

# Occupancies are shared between space... let's build a function block to relate them

open_office_occ_control = OccupancyControl(
    label="OpenOffice Occ Control",
    comment="Occupancy sensor drives LightingZone1 and LightingZone2",
)
open_office_occ_control > ld.openoffice_movement
open_office_occ_control >> ls.lighting_zone_1
open_office_occ_control >> ls.lighting_zone_2
open_office_occ_control.hasOccupancyStatus = OccupancyStatus(hasValue=1)

kitchenette_occ_control = OccupancyControl(
    label="Kitchenette Occ Control",
    comment="Deal with OccupancySpace6...probably not required but it's defined",
)
kitchenette_occ_control > ld.kitchenette_movement
kitchenette_occ_control >> ls.lighting_zone_6
kitchenette_occ_control.hasOccupancyStatus = OccupancyStatus(hasValue=0)

private_office_occ_control = OccupancyControl(
    label="Private Office Occ Control",
    comment="Deal with OccupancySpace3...probably not required but it's defined",
)
private_office_occ_control > ld.privateoffice_movement
private_office_occ_control >> ls.lighting_zone_4
private_office_occ_control.hasOccupancyStatus = OccupancyStatus(hasValue=1)

bathroom_occ_control = OccupancyControl(
    label="Bathroom Occ Control", comment="Light space O2"
)
bathroom_occ_control > ld.bathroom_movement
bathroom_occ_control >> ls.lighting_zone_3
bathroom_occ_control.hasOccupancyStatus = OccupancyStatus(hasValue=1)

corridor_occ_control = OccupancyControl(
    label="Corridor Occ Control", comment="Corridor Light space, O5"
)
corridor_occ_control > ld.corridor_movement
corridor_occ_control >> ls.lighting_zone_5
corridor_occ_control.hasOccupancyStatus = OccupancyStatus(hasValue=1)
