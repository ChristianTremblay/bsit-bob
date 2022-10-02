lighting_zones = {}
# creating the lighting zones and subzones with a system containing a single light_fixtures device serving them.
for zn in (
    lighting_sys_df["Location"].dropna().unique()
):  # creating the lighting zones I can't find rooms for too.
    lighting_zones[zn] = Lighting_Zone(label=zn)
    group = lighting_sys_df.groupby("Location").get_group(zn)
    for i, subzn in enumerate(group["Zone Name"]):
        lighting_zones[zn + subzn] = Lighting_Zone(label=zn + "." + subzn)
        lighting_zones[zn] > lighting_zones[zn + subzn]
        lsys = Zone_Lighting(label=zn + "." + subzn)
        lsys.TotalWattage.hasValue = group.iloc[i]["Total Wattage"]
        lsys.add_serves(lighting_zones[zn + subzn])
        fixt = Light_Fixtures(label=lsys.label + "." + "Fixtures")
        fixt.LoadType.hasValue = group.iloc[i]["Load Type"]
        fixt.FixtureQty.hasValue = group.iloc[i]["Fixture (Qty)"]
        fixt.FixtureWattage.hasValue = group.iloc[i]["Fixture Wattage"]
        lsys > fixt


all_rooms = {}
# Creating every room and containing them in the 3rd or 4th floor. This doesn't include more details about the space or the few lighting domain subspaces
for i, rm in enumerate(lighting_spaces_df.Room_Number.dropna()):
    if rm[0].isdigit():
        all_rooms[rm] = PhysicalSpace(label="room_" + rm)
        rm_sqft = Area(lighting_spaces_df.SquareFootage[i])
        all_rooms[rm].add_property(rm_sqft)
        all_rooms[rm + "L"] = DomainSpace(label=rm + "Lighting")
        all_rooms[rm + "L"].hasDomain = Lighting
        all_rooms[rm] > all_rooms[rm + "L"]
        if pd.isna(lighting_spaces_df.loc[i, "New Area Name"]):
            continue
        if "." in lighting_spaces_df.loc[i, "New Area Name"]:
            continue
        lighting_zones[lighting_spaces_df.loc[i, "New Area Name"]] > all_rooms[rm + "L"]

        if int(rm[0]) == 3:
            Floor3 > all_rooms[rm]
        if int(rm[0]) == 4:
            Floor4 > all_rooms[rm]


lighting_sens_df = pd.read_csv("~/Desktop/223p/LP/b59_lighting_sensors.csv")
lsens = {}
for i, sn in enumerate(lighting_sens_df["Sensor Name"]):
    lsens[sn] = Daylight_Sensor(label=sn)
    lsens[sn].hasMeasurementLocation = lighting_zones[
        lighting_sens_df.Location[i]
    ]  # making the zone the measurement location of the Sensor
    lighting_zones[lighting_sens_df.Location[i]].add_property(lsens[sn].illuminance)


zone_df = pd.read_csv(
    "/Users/lazlopaul/Desktop/brick/LPbricktesting/b59_UFT_ahu_rm.csv"
)

# This is kind of a guess at how the building works
p3 = UFPlenum(
    label="Floor_3.UFPlenum"
)  # A plenum for both floors??? Break it into segments? Multiple plenums on each floor?
p4 = UFPlenum(label="Floor_4.UFPlenum")

r_mat = {}  # rtu matrix
r_mat["rtus"] = {}  # rooftop units
r_mat["rtu_supply"] = {}
r_mat["rtu_return"] = {}
r_mat["rtu_return_zone_F3"] = {}
r_mat["rtu_return_zone_F4"] = {}
r_mat["rtu_return_junction_F3"] = {}
r_mat["rtu_return_junction_F4"] = {}
r_mat["rtu_return_splitter"] = {}
for i in range(1, 5):
    r_mat["rtus"][i] = RooftopUnit(label="RTU_" + str(i))
    r_mat["rtu_supply"][i] = Segment(label="RTU_" + str(i) + ".Supply_Duct")
    # r_mat['rtu_supply'][i].hasRole = Supply
    r_mat["rtu_return"][i] = Segment(
        label="RTU_" + str(i) + ".Return_Duct"
    )  # not sure if this is strictly needed
    # r_mat['rtu_return'][i].hasRole = Return
    # not sure if there should be junction or individual connection points for each RTU
    # NOT SURE I"M USING SEGMENTS OR LNX CORRECTLY
    r_mat["rtu_return"][i].link_to(
        r_mat["rtus"][i].returnAirInlet.mapsTo
    )  # I AM USING THE MAPS TO BECAUSE THATS WHAT WORKS FOR JUNCTIONS, NOT SURE IF I"M MISSING SOMETHING
    pj = Junction(label="PlenumJunction" + ".RTU_" + str(i) + ".supplyInlet")
    r_mat["rtu_supply"][i].link_to(r_mat["rtus"][i].supplyAirOutlet.mapsTo)
    r_mat["rtu_supply"][i].link_to(pj)
    pj.link_to(p3)
    pj.link_to(p4)
    # I would imagine that it'd be good to have plenum  as a subclass for usability.
    # It seems that the plenum is more like a junction than a segment
    # Having difficulty connecting a segment to a system connection point.
    r_mat["rtu_return_zone_F3"][i] = ReturnZone(
        label="RTU_" + str(i) + ".Floor_3.Return_Zone"
    )
    r_mat["rtu_return_zone_F4"][i] = ReturnZone(
        label="RTU_" + str(i) + ".Floor_4.Return_Zone"
    )
    r_mat["rtu_return_junction_F3"][i] = Junction(
        label="RTU_" + str(i) + ".Floor_3.Return_Vent"
    )
    r_mat["rtu_return_junction_F4"][i] = Junction(
        label="RTU_" + str(i) + ".Floor_4.Return_Vent"
    )
    r_mat["rtu_return_zone_F3"][i].returnAirInlet.mapsTo = r_mat[
        "rtu_return_junction_F3"
    ][i]
    r_mat["rtu_return_zone_F4"][i].returnAirInlet.mapsTo = r_mat[
        "rtu_return_junction_F4"
    ][i]
    # This isn't as parallel construction to the UFT because there is not a junction both at the border of the system and the zone
    r_mat["rtu_return_splitter"][i] = Junction(label="RTU_" + str(i) + ".Return_Split")
    r_mat["rtu_return_splitter"][i].link_to(r_mat["rtu_return_junction_F3"][i])
    r_mat["rtu_return_splitter"][i].link_to(r_mat["rtu_return_junction_F4"][i])
    r_mat["rtu_return_splitter"][i].link_to(r_mat["rtu_return"][i])

for i, zn in enumerate(zone_df["Rooms"]):  # iterating through UFTs
    rooms = [rm.strip() for rm in zn.split(",")]  # getting list of rooms for UFT

    uft = UFT(
        label=zone_df.iloc[i]["UFT"]
    )  # creating UFT with points, as well as zone and zone sensors
    # creating normal UFT's for each zone (not sure how to determine the different UFTs at this moment)
    zone = UFTZone(label=zone_df.iloc[i]["UFT"])
    supply_junction = Junction(label=zone_df.iloc[i]["UFT"] + ".junction")
    zone.supplyAir.mapsTo = supply_junction
    uft.add_serves(zone)
    if bool(zone_df.iloc[i]["hasCO2"]):  # some zones have a CO2 concentration
        co2conc = CO2Concentration()
        zone.add_property(co2conc)

    if (
        zone_df.iloc[i]["Floor_Number"] == 3
    ):  # plenum 3 air goes into UFT, and is returned to return duct from zone
        p3.link_to(supply_junction)
    elif zone_df.iloc[i]["Floor_Number"] == 4:
        p4.link_to(supply_junction)
    else:
        raise ValueError("no valid floor number")
    # ZONE FED BY UFT
    # IF A AND D ARE LISTED IN ROOMS, ADDING B AND C. Below is stupid and convoluted
    if (
        ("A" in "".join(rooms))
        & ("D" in "".join(rooms))
        & ~("B" in "".join(rooms))
        & ~("C" in "".join(rooms))
    ):
        rm_base = [rm_base for rm_base in rooms if "A" in rm_base][0][:-1]
        rooms = rooms + [rm_base + "B", rm_base + "C"]
    for j, room_label in enumerate(rooms):
        HVACroom = DomainSpace(
            label=room_label
        )  # I am not sure yet how DomainSpace and Physical Space should Interact here. Just making physical space contain a domain space.
        HVACroom.hasDomain = HVAC
        if room_label in all_rooms.values():
            all_rooms[room_label] > HVACroom
        zone > HVACroom  # This should be encloses rather than contains now I think
        room_supply_cp = AirInletConnectionPoint(
            HVACroom, label=HVACroom.label + ".supplyAir"
        )
        room_return_cp = AirOutletConnectionPoint(
            HVACroom, label=HVACroom.label + ".returnAir"
        )
        supply_junction.link_to(room_supply_cp)

        if zone_df.iloc[i]["Floor_Number"] == 3:
            r_mat["rtu_return_junction_F3"][zone_df.iloc[i]["ahuRef"]].connect_to(
                room_return_cp
            )  # getting the return junction for the correct floor and ahu
        elif zone_df.iloc[i]["Floor_Number"] == 4:
            r_mat["rtu_return_junction_F4"][zone_df.iloc[i]["ahuRef"]].connect_to(
                room_return_cp
            )
        else:
            raise ValueError("no valid floor number")

            # should the rooms have their own domain spaces, or should they be contained by a single domain space. How do I do air inlet if I have multiple domain spaces in zone, can't map like in HVACZone1

            # Domain space is bigger than room. Currently physical spaces enclose domain spaces, not vice versa. Here the domainspace is bigger than all of the sensible physical spaces.

# Instantiating Water System, this may prompt a lot of questions for s223 strike team
CWS = CoolingWaterSystem(label="Cooling_Water_System")
CTS = CoolingTowerSystem(label="Cooling_Tower_System")
CWS.CWReturn << CTS.waterOutlet  # check this connection
SSF = SSFSystem(CTS, label="SSF_System")
# Not further instantiating water connections (connecting chilled water to coils) because I don't understand the nature of those connections
# No information on boiler, so not included at this time

# ADDING CORE ZONES


lbnl_header(model_name)

dump()
