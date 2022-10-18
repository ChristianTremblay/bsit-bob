from pathlib import Path

import hvac_devices as hd
import hvac_spaces as hs
import lighting_devices as ld
import lighting_spaces as ls

from bob.core import UNIT, bind_model_namespace, dump
from bob.functions import FunctionBlock, G36AnalogInput, G36AnalogOutput
from bob.functions.occupancy import OccupancyFunction
from bob.properties import Temperature
from bob.properties.states import OccupancyStatus, Schedule
from bob.sensor.temperature import TemperatureSensor

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


class Average(FunctionBlock):
    """
    y = (u1 + u2) / 2.0
    """

    u1: G36AnalogInput
    u2: G36AnalogInput
    y: G36AnalogOutput


# make an instance
f = Average(label="FB-1", comment="Compute DA-T Avg")

# line up the input(s)
hd.ahu["DA-T"].observesProperty >> f.u1

# line up the output to a special property
f_avg_temp = Temperature(label="DA-T-AVG", hasValue=0, unit=UNIT.DEG_C)
f.y >> f_avg_temp


#
#   Open Office
#

open_office_occ_control = OccupancyFunction(
    label="Open Office Occ Control",
    comment="Occupancy sensor drives LightingZone1 and LightingZone2",
)
open_office_occ_control_schedule = Schedule(label="Open Office Occ Schedule")

ld.openoffice_movement.observesProperty >> open_office_occ_control.inStatus
open_office_occ_control_schedule >> open_office_occ_control.inSchedule

open_office_occ_control.outStatus >> ls.lighting_zone_1.occupancy
open_office_occ_control.outStatus >> ls.lighting_zone_2.occupancy
open_office_occ_control.outStatus >> hs.openoffice_hvac.occupancy

#
#   Kitchenette
#

kitchenette_occ_control = OccupancyFunction(
    label="Kitchenette Occ Control",
    comment="Occupancy sensor drives LightingZone1 and LightingZone2",
)
kitchenette_occ_control_schedule = Schedule(label="Kitchenette Occ Schedule")

ld.kitchenette_movement.observesProperty >> kitchenette_occ_control.inStatus
kitchenette_occ_control_schedule >> kitchenette_occ_control.inSchedule

kitchenette_occ_control.outStatus >> ls.lighting_zone_6.occupancy
kitchenette_occ_control.outStatus >> hs.hvac_zone_2.occupancy

#
#   Private Office
#

private_office_occ_control = OccupancyFunction(
    label="Private Office Occ Control",
    comment="Deal with OccupancySpace3...probably not required but it's defined",
)
private_office_occ_control_schedule = Schedule(label="Private Office Occ Schedule")

ld.privateoffice_movement.observesProperty >> private_office_occ_control.inStatus
private_office_occ_control_schedule >> private_office_occ_control.inSchedule

private_office_occ_control.outStatus >> ls.lighting_zone_4.occupancy
private_office_occ_control.outStatus >> hs.privateoffice_hvac.occupancy

#
#   Bathroom
#

bathroom_occ_control = OccupancyFunction(
    label="Bathroom Occ Control",
    comment="Light space O2",
)
bathroom_occ_control_schedule = Schedule(label="Bathroom Occ Schedule")

ld.bathroom_movement.observesProperty >> bathroom_occ_control.inStatus
bathroom_occ_control_schedule >> bathroom_occ_control.inSchedule

bathroom_occ_control.outStatus >> ls.lighting_zone_3.occupancy
bathroom_occ_control.outStatus >> hs.bathroom_hvac.occupancy

#
#   Corridor
#

corridor_occ_control = OccupancyFunction(
    label="Corridor Occ Control",
    comment="Corridor Light space, O5",
)
corridor_occ_control_schedule = Schedule(label="Corridor Occ Schedule")

ld.corridor_movement.observesProperty >> corridor_occ_control.inStatus
corridor_occ_control_schedule >> corridor_occ_control.inSchedule

corridor_occ_control.outStatus >> ls.lighting_zone_5.occupancy
corridor_occ_control.outStatus >> hs.corridorNorth_hvac.occupancy
