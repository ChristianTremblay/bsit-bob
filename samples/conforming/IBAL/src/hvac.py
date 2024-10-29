from pathlib import Path

import hvac_devices as hd
import hvac_spaces as hs

from bob.connections.air import AirConnection
from bob.core import UNIT, bind_model_namespace, dump
from bob.properties.states import OnOffCommand, OnOffStatus
from bob.sensor.temperature import Temperature

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}:{model_name}/")


outdoor = AirConnection(
    label="Outdoor",
    comment="This is where we exhaust air of bathroom, and windows of OpenOffice are connected here to",
)

plenum = AirConnection(
    label="Plenum",
    comment="Air around units, mostly to reference low static pressure port of differential pressure sensor",
)

ahu3_mixedAir = AirConnection(
    label="MixedAirDuct",
    comment="Mix between return air and outdoor air",
)

ahu3_exhaust_return_air = AirConnection(
    label="Exhaust&ReturnMixedAirDuct",
    comment="Mix between return air and exhaust air",
)

ahu3_supplyAir = AirConnection(
    label="MixedAirDuct",
    comment="Mix between return air and outdoor air",
)

ahu1and2_supplyAir = AirConnection(
    label="SUPPLY-DUCT", comment="Supply Air Duct that feed AHU1 & 2"
)

ahu1_mixedAir = AirConnection(
    label="MixedAirDuct",
    comment="Mix between return air and outdoor air",
)

ahu2_mixedAir = AirConnection(
    label="MixedAirDuct",
    comment="Mix between return air and outdoor air",
)

ahu1_supplyAir = AirConnection(
    label="SUPPLY-DUCT", comment="Supply Air Duct that feed AHU1 & 2"
)

ahu2_supplyAir = AirConnection(
    label="SUPPLY-DUCT", comment="Supply Air Duct that feed AHU1 & 2"
)

ahu1_returnAir = AirConnection(
    label="Z1&2_RETURN-DUCT", comment="Return Air Duct after Zones 1 and 2"
)

ahu2_returnAir = AirConnection(
    label="Z3&4_RETURN-DUCT", comment="Return Air Duct after Zones 3 and 4"
)

fan3_mixedAir = AirConnection(label="fan3_misedAir", comment="before fan3")
fan4_mixedAir = AirConnection(label="fan4_misedAir", comment="before fan4")

# AHU3
outdoor >> hd.ahu3["OADPR_d19"].airInlet

hd.ahu3["OADPR_d19"] >> ahu3_mixedAir
hd.ahu3["MADPR_d8"] >> ahu3_mixedAir
(
    ahu3_mixedAir
    >> hd.ahu3["FILTER"]
    >> hd.ahu3["CLGCOIL"]
    >> hd.ahu3["HTGCOIL"]
    >> hd.ahu3["SF"]
    >> ahu3_supplyAir
)

ahu3_supplyAir >> hd.damper16 >> ahu3_exhaust_return_air
ahu3_exhaust_return_air >> hd.ahu3["MADPR_d8"]
ahu3_exhaust_return_air >> hd.ahu3["EADPR_d17"]
hd.ahu3["EADPR_d17"].airOutlet >> outdoor

ahu3_supplyAir >> hd.damper15.airInlet
hd.damper15.airOutlet >> ahu1and2_supplyAir

ahu1and2_supplyAir >> hd.ahu1["OADPR_d6"]
ahu1and2_supplyAir >> hd.ahu2["OADPR_d7"]

hd.ahu1["OADPR_d6"].airOutlet >> ahu1_mixedAir
hd.ahu1["MADPR_d5"].airOutlet >> ahu1_mixedAir
(
    ahu1_mixedAir
    >> hd.ahu1["FILTER"]
    >> hd.ahu1["HTGCOIL"]
    >> hd.ahu1["CLGCOIL"]
    >> hd.ahu1["SF"]
    >> ahu1_supplyAir
)
ahu1_supplyAir >> hd.damper5a.airInlet
hd.damper5a.airOutlet >> ahu2_supplyAir
ahu1_supplyAir >> hd.vav1["DPR"].airInlet
ahu1_supplyAir >> hd.vav2["DPR"].airInlet
hd.vav1["REHEAT"].airOutlet >> hs.zone1_hvac.ductAirInlet
hd.vav2["REHEAT"].airOutlet >> hs.zone2_hvac.ductAirInlet

hs.zone1_hvac.ductAirOutlet >> ahu1_returnAir

hs.zone2_hvac.ductAirOutlet >> ahu1_returnAir
ahu1_returnAir >> hd.ahu1["MADPR_d5"].airInlet
(
    ahu1_returnAir
    >> hd.damper6
    >> fan3_mixedAir
    >> hd.fan3
    >> hd.fan3_barometric_damper
    >> outdoor
)
fan3_mixedAir >> hd.damper10a >> fan4_mixedAir

hd.ahu2["OADPR_d7"].airOutlet >> ahu2_mixedAir
hd.ahu2["MADPR_d8"].airOutlet >> ahu2_mixedAir
(
    ahu2_mixedAir
    >> hd.ahu2["FILTER"]
    >> hd.ahu2["HTGCOIL"]
    >> hd.ahu2["CLGCOIL"]
    >> hd.ahu2["SF"]
    >> ahu2_supplyAir
)
ahu2_supplyAir >> hd.damper5b.airInlet
hd.damper5b.airOutlet >> ahu1_supplyAir
ahu2_supplyAir >> hd.vav3["DPR"].airInlet
ahu2_supplyAir >> hd.vav4["DPR"].airInlet
hd.vav3["REHEAT"].airOutlet >> hs.zone3_hvac.ductAirInlet
hd.vav4["REHEAT"].airOutlet >> hs.zone4_hvac.ductAirInlet
hs.zone3_hvac.ductAirOutlet >> ahu2_returnAir
hs.zone4_hvac.ductAirOutlet >> ahu2_returnAir

ahu2_returnAir >> hd.ahu2["MADPR_d8"]

(
    ahu2_returnAir
    >> hd.damper8
    >> fan4_mixedAir
    >> hd.fan4
    >> hd.fan4_barometric_damper
    >> outdoor
)
fan4_mixedAir >> hd.damper10b >> fan3_mixedAir


hd.outdoor_temp % outdoor
hd.outdoor_hum % outdoor
hd.outdoor_pressure % outdoor

# AHU Sensors
hd.ahu1["ahu1_p_up"]["highPort"] % hd.ahu1["SF"].airInlet
hd.ahu1["ahu1_p_up"]["lowPort"] % plenum
hd.ahu1["ahu1_p_down"]["highPort"] % ahu1_supplyAir
hd.ahu1["ahu1_p_down"]["lowPort"] % plenum
hd.ahu1["ahu1_out_rtd"] % ahu1_supplyAir
hd.ahu1["ahu1_rh_down"] % ahu1_supplyAir
hd.ahu1["ahu1_cc_rtd"] % hd.ahu1["CLGCOIL"].airOutlet
hd.ahu1["ahu1_heat_rtd"] % hd.ahu1["HTGCOIL"].airOutlet
hd.ahu1["ahu1_rh_up"] % hd.ahu1["HTGCOIL"].airInlet
hd.ahu1["ahu1_in_rtd"] % hd.ahu1["HTGCOIL"].airInlet

hd.ahu2["ahu2_p_up"]["highPort"] % hd.ahu2["SF"].airInlet
hd.ahu2["ahu2_p_up"]["lowPort"] % plenum
hd.ahu2["ahu2_p_down"]["highPort"] % ahu2_supplyAir
hd.ahu2["ahu2_p_down"]["lowPort"] % plenum
hd.ahu2["ahu2_out_rtd"] % ahu2_supplyAir
hd.ahu2["ahu2_rh_down"] % ahu2_supplyAir
hd.ahu2["ahu2_cc_rtd"] % hd.ahu2["CLGCOIL"].airOutlet
hd.ahu2["ahu2_heat_rtd"] % hd.ahu2["HTGCOIL"].airOutlet
hd.ahu2["ahu2_rh_up"] % hd.ahu2["HTGCOIL"].airInlet
hd.ahu2["ahu2_in_rtd"] % hd.ahu2["HTGCOIL"].airInlet


hd.ahu3["ahu3_p_up"]["highPort"] % hd.ahu3["SF"].airInlet
hd.ahu3["ahu3_p_up"]["lowPort"] % plenum
hd.ahu3["ahu3_p_down"]["highPort"] % ahu3_supplyAir
hd.ahu3["ahu3_p_down"]["lowPort"] % plenum

hd.ahu3["ahu3_out_rtd"] % ahu3_supplyAir
hd.ahu3["ahu3_rh_down"] % ahu3_supplyAir
hd.ahu3["ahu3_cc_rtd"] % hd.ahu3["CLGCOIL"].airOutlet
hd.ahu3["ahu3_heat_rtd"] % hd.ahu3["HTGCOIL"].airOutlet
hd.ahu3["ahu3_in_rtd"] % hd.ahu3["CLGCOIL"].airInlet

# Flow
hd.ahu1["ahu1_in_flow"] % hd.ahu1["OADPR_d6"].airInlet
hd.ahu2["ahu2_in_flow"] % hd.ahu2["OADPR_d7"].airInlet

hd.vav1["ZN-T"] % hs.zone1_hvac
hd.vav2["ZN-T"] % hs.zone2_hvac
hd.vav3["ZN-T"] % hs.zone3_hvac
hd.vav4["ZN-T"] % hs.zone4_hvac


"""
NOT READY TO DO THAT

hd.chiller.chilledWaterLeaving >> hd.chilled_water_pump.waterInlet
hd.chilled_water_pump.waterOutlet >> hd.ahu1["CLGCOIL"].chilledWaterInlet
hd.ahu1["CLGCOIL"].chilledWaterOutlet >> hd.clg_vlv["valve"].waterInlet
hd.clg_vlv["valve"].waterOutlet >> hd.chiller.chilledWaterEntering

"""


if __name__ == "__main__":
    dump()
