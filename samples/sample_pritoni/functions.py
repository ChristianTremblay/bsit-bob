from pathlib import Path

import hvac_devices as hd
import hvac_spaces as hs
import lighting_devices as ld
import lighting_spaces as ls

from bob.core import bind_model_namespace, UNIT
from bob.functions import FunctionBlock
from bob.functions.occupancy import OccupancyControl
from bob.properties import Temperature
from bob.properties.states import OccupancyStatus, Schedule
from bob.sensor.temperature import TemperatureSensor

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


class AVG_Temp(FunctionBlock):
    avg_tmp: Temperature


f = AVG_Temp(label="FB-1", comment="Compute DA-T Avg")
f.avg_tmp = Temperature(hasValue=0, unit=UNIT.DEG_C)
f.uses(hd.ahu["DA-T"].observesProperty)
f.produces(f.avg_tmp)


open_office_occ_control = OccupancyControl(
    label="OpenOffice Occ Control",
    comment="Occupancy sensor drives LightingZone1 and LightingZone2",
    schedule=Schedule(),
    occupancyStatus=OccupancyStatus(),
)
open_office_occ_control.produces(ls.lighting_zone_1.occupancy)
open_office_occ_control.produces(ls.lighting_zone_2.occupancy)
open_office_occ_control.produces(hs.openoffice_hvac.occupancy)
open_office_occ_control.uses(open_office_occ_control.schedule)
open_office_occ_control.uses(ld.openoffice_movement.observesProperty)

kitchenette_occ_control = OccupancyControl(
    label="Kitchenette Occ Control",
    comment="Deal with OccupancySpace6...probably not required but it's defined",
    schedule=Schedule(),
    occupancyStatus=OccupancyStatus(),
)
# kitchenette_occ_control > ld.kitchenette_movement
kitchenette_occ_control.produces(ls.lighting_zone_6.occupancy)
kitchenette_occ_control.produces(hs.hvac_zone_2.occupancy)
kitchenette_occ_control.uses(kitchenette_occ_control.schedule)
kitchenette_occ_control.uses(ld.kitchenette_movement.observesProperty)

private_office_occ_control = OccupancyControl(
    label="Private Office Occ Control",
    comment="Deal with OccupancySpace3...probably not required but it's defined",
    schedule=Schedule(),
    occupancyStatus=OccupancyStatus(),
)
# private_office_occ_control > ld.privateoffice_movement
private_office_occ_control.produces(ls.lighting_zone_4.occupancy)
private_office_occ_control.produces(hs.privateoffice_hvac.occupancy)
private_office_occ_control.uses(private_office_occ_control.schedule)
private_office_occ_control.uses(ld.privateoffice_movement.observesProperty)

bathroom_occ_control = OccupancyControl(
    label="Bathroom Occ Control",
    comment="Light space O2",
    schedule=Schedule(),
    occupancyStatus=OccupancyStatus(),
)
# bathroom_occ_control > ld.bathroom_movement
bathroom_occ_control.produces(ls.lighting_zone_3.occupancy)
bathroom_occ_control.produces(hs.bathroom_hvac.occupancy)
bathroom_occ_control.uses(bathroom_occ_control.schedule)
bathroom_occ_control.uses(ld.bathroom_movement.observesProperty)

corridor_occ_control = OccupancyControl(
    label="Corridor Occ Control",
    comment="Corridor Light space, O5",
    schedule=Schedule(),
    occupancyStatus=OccupancyStatus(),
)
# corridor_occ_control > ld.corridor_movement
corridor_occ_control.produces(ls.lighting_zone_5.occupancy)
corridor_occ_control.produces(hs.corridorNorth_hvac.occupancy)
corridor_occ_control.uses(corridor_occ_control.schedule)
corridor_occ_control.uses(ld.corridor_movement.observesProperty)
