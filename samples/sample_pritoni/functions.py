from pathlib import Path

import hvac_devices as hd
import hvac_spaces as hs
import lighting_devices as ld
import lighting_spaces as ls

from bob.core import FunctionBlock, bind_model_namespace, unit
from bob.functions.occupancy import OccupancyControl
from bob.properties import Temperature
from bob.properties.states import OccupancyStatus, Schedule
from bob.sensor.temperature import TemperatureSensor

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


class AVG_Temp(FunctionBlock):
    avg_tmp: Temperature


f = AVG_Temp(label="FB-1", comment="Compute DA-T Avg")
f.avg_tmp = Temperature(hasValue=0, unit=unit.DEG_C)
f.uses_input(hd.ahu["DA-T"].observesProperty)
f.produces_output(f.avg_tmp)


open_office_occ_control = OccupancyControl(
    label="OpenOffice Occ Control",
    comment="Occupancy sensor drives LightingZone1 and LightingZone2",
    hasSchedule=Schedule(),
    hasOccupancyStatus=OccupancyStatus(),
)
open_office_occ_control.produces_output(ls.lighting_zone_1.occupancy)
open_office_occ_control.produces_output(ls.lighting_zone_2.occupancy)
open_office_occ_control.produces_output(hs.openoffice_hvac.occupancy)
open_office_occ_control.uses_input(open_office_occ_control.hasSchedule)
open_office_occ_control.uses_input(ld.openoffice_movement.observesProperty)

kitchenette_occ_control = OccupancyControl(
    label="Kitchenette Occ Control",
    comment="Deal with OccupancySpace6...probably not required but it's defined",
    hasSchedule=Schedule(),
    hasOccupancyStatus=OccupancyStatus(),
)
# kitchenette_occ_control > ld.kitchenette_movement
kitchenette_occ_control.produces_output(ls.lighting_zone_6.occupancy)
kitchenette_occ_control.produces_output(hs.hvac_zone_2.occupancy)
kitchenette_occ_control.uses_input(kitchenette_occ_control.hasSchedule)
kitchenette_occ_control.uses_input(ld.kitchenette_movement.observesProperty)

private_office_occ_control = OccupancyControl(
    label="Private Office Occ Control",
    comment="Deal with OccupancySpace3...probably not required but it's defined",
    hasSchedule=Schedule(),
    hasOccupancyStatus=OccupancyStatus(),
)
# private_office_occ_control > ld.privateoffice_movement
private_office_occ_control.produces_output(ls.lighting_zone_4.occupancy)
private_office_occ_control.produces_output(hs.privateoffice_hvac.occupancy)
private_office_occ_control.uses_input(private_office_occ_control.hasSchedule)
private_office_occ_control.uses_input(ld.privateoffice_movement.observesProperty)

bathroom_occ_control = OccupancyControl(
    label="Bathroom Occ Control",
    comment="Light space O2",
    hasSchedule=Schedule(),
    hasOccupancyStatus=OccupancyStatus(),
)
# bathroom_occ_control > ld.bathroom_movement
bathroom_occ_control.produces_output(ls.lighting_zone_3.occupancy)
bathroom_occ_control.produces_output(hs.bathroom_hvac.occupancy)
bathroom_occ_control.uses_input(bathroom_occ_control.hasSchedule)
bathroom_occ_control.uses_input(ld.bathroom_movement.observesProperty)

corridor_occ_control = OccupancyControl(
    label="Corridor Occ Control",
    comment="Corridor Light space, O5",
    hasSchedule=Schedule(),
    hasOccupancyStatus=OccupancyStatus(),
)
# corridor_occ_control > ld.corridor_movement
corridor_occ_control.produces_output(ls.lighting_zone_5.occupancy)
corridor_occ_control.produces_output(hs.corridorNorth_hvac.occupancy)
corridor_occ_control.uses_input(corridor_occ_control.hasSchedule)
corridor_occ_control.uses_input(ld.corridor_movement.observesProperty)
