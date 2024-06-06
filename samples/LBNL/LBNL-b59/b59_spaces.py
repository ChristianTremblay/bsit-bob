from __future__ import annotations

from pathlib import Path
from typing import Any

# from bob.domain import *
import pandas as pd
from b59_HVAC import *
from header import lbnl_header

from bob.connections.air import *
from bob.connections.liquid import *
from bob.core import (
    HVAC,
    Air,
    DomainSpace,
    Equipment,
    Junction,
    System,
    bind_model_namespace,
    dump,
    p223,
    QUANTITYKIND,
    UNIT,
)
from bob.equipment.archives.coolingcoil import ChilledWaterCoil, ChilledWaterCoil2
from bob.equipment.archives.heatingcoil import HotWaterCoil2
from bob.equipment.hvac.airflowstation import AirFlowMonitor
from bob.equipment.hvac.damper import Damper
from bob.equipment.hvac.fan import Fan
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.vfd import VFD
from bob.role import Exhaust, Return, Supply

# from bob.signal import(
#     AnalogOut,
#     AnalogIn,
#     )


# model_name = Path(__file__).stem
model_name = "b59"
_namespace = ex = bind_model_namespace(
    "ex", f"http://data.ashrae.org/standard223/data/{model_name}#"
)


# qudt = bind_namespace("qudt", "http://qudt.org/schema/qudt/")
# quantitykind = bind_namespace("quantitykind", "http://qudt.org/vocab/quantitykind/")

# class Area(QuantifiableObservableProperty):
#     hasUnits = qudt.FT2
#     hasQuantityKind = quantitykind.Area
#     def __init__(self, *args: Any, **kwargs: Any) -> None:
#         super().__init__(*args, **kwargs)


class Plenum(DomainSpace):
    cp1: AirBidirectionalConnectionPoint
    cp2: AirBidirectionalConnectionPoint
    supplyInlet: AirInletConnectionPoint
    hasDomain = HVAC


class CeilingSpace(DomainSpace):
    returnOutlet: AirOutletConnectionPoint
    hasDomain = HVAC


lighting_spaces_df = pd.read_csv("~/Desktop/223p/LP/b59_lighting_spaces_v4.csv")
lighting_sys_df = pd.read_csv("~/Desktop/223p/LP/b59_lighting_v2.csv")
lighting_spaces_df = lighting_spaces_df.drop_duplicates(
    subset=["Room_Number"], keep="last"
)
Floor3 = PhysicalSpace(label="Floor_3")
Floor4 = PhysicalSpace(label="Floor_4")

all_rooms = {}
# Creating every room and containing them in the 3rd or 4th floor. This doesn't include more details about the space or the few lighting domain subspaces
for i, row in lighting_spaces_df.iterrows():
    rm = str(row.Room_Number)
    if str(rm)[0].isdigit():
        all_rooms[rm] = PhysicalSpace(label=rm)
        # rm_sqft = Area(row.SquareFootage)
        # all_rooms[rm].add_property(rm_sqft)
        if pd.isna(row["New Area Name"]):
            continue
        if "." in row["New Area Name"]:
            continue
        if int(rm[0]) == 3:
            Floor3 > all_rooms[rm]
        if int(rm[0]) == 4:
            Floor4 > all_rooms[rm]


zone_df = pd.read_csv(
    "/Users/lazlopaul/Desktop/brick/LPbricktesting/b59_UFT_ahu_rm2.csv"
)
r_mat = {}  # rtu matrix
r_mat["rtus"] = {}  # rooftop units
for i in range(1, 5):
    r_mat[i] = RooftopUnit(label="RTU_" + str(i))

plenum = {}  # plenum[Floor][RTU]
ceiling_space = {}
core_zones = {}
for floor in range(3, 5):
    plenum[floor] = {}
    ceiling_space[floor] = {}
    core_zones[floor] = {}
    for rtu in range(1, 5):
        # creating plenums for each RTU and connecting them to each other
        core_zones[floor][rtu] = Zone(
            label="Floor_{}.RTU_{}.CoreZone".format(floor, rtu)
        )
        core_zones[floor][rtu].hasDomain = HVAC
        plenum[floor][rtu] = Plenum(label="Floor_{}.RTU_{}.Plenum".format(floor, rtu))
        ceiling_space[floor][rtu] = CeilingSpace(
            label="Floor_{}.RTU_{}.Ceiling".format(floor, rtu)
        )
        if rtu > 1:
            plenum[floor][rtu - 1].cp2 >> plenum[floor][rtu].cp1
            plenum[floor][rtu - 1].cp2.connectedFrom = plenum[floor][rtu].cp1
            plenum[floor][rtu].cp1.connectedTo = plenum[floor][rtu - 1].cp2
        # connecting plenums to RTU
        if floor == 3:
            r_mat[rtu].supplyAirOutlet >> plenum[floor][rtu].supplyInlet
            r_mat[rtu].returnAirInlet << ceiling_space[floor][rtu].returnOutlet
        else:
            (
                r_mat[rtu].supplyAirOutlet.mapsTo.connectsThrough
                >> plenum[floor][rtu].supplyInlet
            )
            (
                r_mat[rtu].returnAirInlet.mapsTo.connectsThrough
                << ceiling_space[floor][rtu].returnOutlet
            )

        r_mat[rtu] >> core_zones[floor][rtu]

uft_rooms = []
ufts = {}
uftzones = {}
HVACrooms = {}
for i, row in zone_df.iterrows():  # iterating through UFTs
    rooms = [
        rm.strip() for rm in row["Rooms"].split(",")
    ]  # getting list of rooms for UFT
    ufts[row["UFT"]] = UFT(
        label=row["UFT"]
    )  # creating UFT with points, as well as zone and zone sensors
    # creating normal UFT's for each zone (not sure how to determine the different UFTs at this moment)
    uftzones[row["UFT"]] = UFTZone(label=row["UFT"] + ".zone")
    ufts[row["UFT"]] >> uftzones[row["UFT"]]
    if bool(row["hasCO2"]):  # some zones have a CO2 concentration
        co2conc = CO2Concentration()
        uftzones[row["UFT"]].add_property(co2conc)
    floor_ind = row["Floor_Number"]
    ahu_ind = row["ahuRef"]
    plen_cp = AirOutletConnectionPoint(plenum[floor_ind][ahu_ind])
    plen_cp >> ufts[row["UFT"]].supplyAirInlet

    # IF A AND D ARE LISTED IN ROOMS, ADDING B AND C. Below is stupid and convoluted
    if (
        ("A" in "".join(rooms))
        & ("D" in "".join(rooms))
        & ~("B" in "".join(rooms))
        & ~("C" in "".join(rooms))
    ):
        rm_base = [rm_base for rm_base in rooms if "A" in rm_base][0][:-1]
        rooms = rooms + [rm_base + "B", rm_base + "C"]
        rooms = list(set(rooms))
    for j, room_label in enumerate(rooms):
        uft_rooms.append(room_label)

        if room_label not in HVACrooms.keys():
            HVACrooms[room_label] = DomainSpace(
                label=room_label
            )  # I am not sure yet how DomainSpace and Physical Space should Interact here. Just making physical space contain a domain space.
            HVACrooms[room_label].hasDomain = HVAC
            all_rooms[room_label] > HVACrooms[room_label]

        uftzones[row["UFT"]] > HVACrooms[room_label]
        room_supply_cp = AirInletConnectionPoint(
            HVACrooms[room_label], label=HVACrooms[room_label].label + ".supplyAir"
        )
        room_return_cp = AirOutletConnectionPoint(
            HVACrooms[room_label], label=HVACrooms[room_label].label + ".returnAir"
        )
        try:
            ufts[row["UFT"]].supplyAirOutlet.mapsTo.connectsThrough >> room_supply_cp
        except:
            ufts[row["UFT"]].supplyAirOutlet >> room_supply_cp

        ceil_cp = AirInletConnectionPoint(ceiling_space[floor_ind][ahu_ind])
        room_return_cp >> ceil_cp

# Instantiating Water System, this may prompt a lot of questions for s223 strike team
CWS = CoolingWaterSystem(label="Cooling_Water_System")
CTS = CoolingTowerSystem(label="Cooling_Tower_System")
CWS.CWReturn << CTS.waterOutlet  # check this connection
SSF = SSFSystem(CTS, label="SSF_System")


lbnl_header(model_name)

dump()
