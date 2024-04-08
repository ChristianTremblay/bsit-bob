from pathlib import Path

import hvac_spaces as hs

from bob.connections.electricity import (
    Electricity_120VLN_1Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from bob.core import UNIT, Role, bind_model_namespace, dump
from bob.equipment.architectural import Window

from bob.equipment.hvac.airhandlingunit import AirHandlingUnit
from bob.equipment.hvac.boiler import ElectricalHotWaterBoiler
from bob.equipment.hvac.chiller import Chiller
from bob.equipment.hvac.coil import (
    ChilledWaterCoil,
    Coil,
    ElectricalHeatingCoil,
    HotWaterCoil,
)
from bob.equipment.hvac.damper import (
    ElectricalActuatedProportionalDamper,
    GravityDamper,
)

from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.pump import Pump, PumpWithStarter
from bob.equipment.hvac.stats import AirDifferentialStaticPressureSensor
from bob.equipment.hvac.valve import (
    ThreeWayDivertingActuatedProportionalValve,
    TwoWayActuatedProportionalValve,
)
from bob.equipment.hvac.vav import VAV_Reheat
from bob.sensor.flow import AirFlowSensor
from bob.sensor.humidity import AirHumiditySensor, RelativeHumidity
from bob.sensor.pressure import DifferentialStaticPressure
from bob.sensor.temperature import AirTemperatureSensor, Temperature

# Prototypes
from bob.scratch.electricity.starter import MotorStarter_600VLL_3Ph_60Hz as MotorStarter
from bob.scratch.electricity.vfd import VFD
from bob.scratch.hvac.fan import Fan

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


ahu1_template = {
    "params": {
        "label": "AHU1 ",
        "comment": "AHU delivering air to VAV boxes 1 2 3 4 in parallel with AHU 2 (not at the same time, see damper 5)",
    },
    "sensors": {
        ("ahu1_p_down", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Duct static pressure after fan",
        },
        ("ahu1_rh_down", AirHumiditySensor): {
            "comment": "Discharge Air humidity after fan",
        },
        ("ahu1_out_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after fan",
        },
        ("ahu1_cc_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after cooling coil",
        },
        ("ahu1_p_up", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Duct static pressure after cooling coil, before fan",
        },
        ("ahu1_heat_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after heating coil",
        },
        ("ahu1_rh_up", AirHumiditySensor): {
            "comment": "Discharge Air humidity before heating coil",
        },
        ("ahu1_in_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature before heating coil",
        },
        ("ahu1_in_flow", AirFlowSensor): {
            "hasUnit": UNIT["FT3-PER-MIN"],
            "comment": "Air flow before fresh air damper",
        },
    },
    "equipment": {
        ("SF", Fan): {
            "comment": "Supply Air Fan",
            "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            "hasRole": Role.Supply,
        },
        ("SF_VFD", VFD): {
            "comment": "Return Air Fan VFD",
            "electricalOutlet": Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
        },
        ("CLGCOIL", ChilledWaterCoil): {"comment": "Cooling Coil"},
        ("HTGCOIL", ElectricalHeatingCoil): {"comment": "Heating coil"},
        ("FILTER", Filter): {"comment": "Filter"},
        ("OADPR_d6", ElectricalActuatedProportionalDamper): {
            "comment": "Outdoor air damper (d6)"
        },
        ("MADPR_d5", ElectricalActuatedProportionalDamper): {
            "comment": "Mixed Air Damper (d5)"
        },
    },
}

ahu2_template = {
    "params": {
        "label": "AHU2 ",
        "comment": "AHU delivering air to VAV boxes 1 2 3 4 in parallel with AHU 1 (not at the same time, see damper 5)",
    },
    "sensors": {
        ("ahu2_p_down", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Duct static pressure after fan",
        },
        ("ahu2_rh_down", AirHumiditySensor): {
            "comment": "Discharge Air humidity after fan",
        },
        ("ahu2_out_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after fan",
        },
        ("ahu2_cc_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after cooling coil",
        },
        ("ahu2_p_up", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Duct static pressure after cooling coil, before fan",
        },
        ("ahu2_heat_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after heating coil",
        },
        ("ahu2_rh_up", AirHumiditySensor): {
            "comment": "Discharge Air humidity before heating coil",
        },
        ("ahu2_in_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature before heating coil",
        },
        ("ahu2_in_flow", AirFlowSensor): {
            "hasUnit": UNIT["FT3-PER-MIN"],
            "comment": "Air flow before fresh air damper",
        },
    },
    "equipment": {
        ("SF", Fan): {
            "comment": "Supply Air Fan",
            "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            "hasRole": Role.Supply,
        },
        ("SF_VFD", VFD): {
            "electricalOutlet": Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
            "comment": "Return Air Fan VFD",
        },
        ("CLGCOIL", ChilledWaterCoil): {"comment": "Cooling Coil"},
        ("HTGCOIL", ElectricalHeatingCoil): {"comment": "Heating coil"},
        ("FILTER", Filter): {"comment": "Filter"},
        ("OADPR_d7", ElectricalActuatedProportionalDamper): {
            "comment": "Outdoor air damper (d7)"
        },
        ("MADPR_d8", ElectricalActuatedProportionalDamper): {
            "comment": "Mixed Air Damper (d8)"
        },
    },
}

ahu3_template = {
    "params": {"label": "AHU3 ", "comment": "AHU delivering fresh air to AHU1&2)"},
    "sensors": {
        ("ahu3_p_down", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Duct static pressure after fan",
        },
        ("ahu3_rh_down", AirHumiditySensor): {
            "comment": "Discharge Air humidity after fan",
        },
        ("ahu3_out_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after fan",
        },
        ("ahu3_heat_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after reheat coil",
        },
        ("ahu3_p_up", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Duct static pressure after reheat coil, before fan",
        },
        ("ahu3_cc_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after cooling coil",
        },
        ("ahu3_in_rtd", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature before cooling coil",
        },
    },
    "equipment": {
        ("SF", Fan): {
            "comment": "Supply Air Fan",
            "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            "hasRole": Role.Supply,
        },
        ("SF_Starter", MotorStarter): {
            "comment": "Supply Air Fan Starter",
            "electricalOutlet": Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
        },
        ("CLGCOIL", Coil): {"comment": "DX Cooling Coil"},
        ("HTGCOIL", ElectricalHeatingCoil): {"comment": "Reheat coil"},
        ("FILTER", Filter): {"comment": "Filter"},
        ("OADPR_d19", ElectricalActuatedProportionalDamper): {
            "comment": "Outdoor air damper (d19)"
        },
        ("MADPR_d8", ElectricalActuatedProportionalDamper): {
            "comment": "Mixed Air Damper (d18)"
        },
        ("EADPR_d17", GravityDamper): {"comment": "Exhaust Air Damper (d17)"},
    },
}

vav1_config = {
    "params": {"label": "VAVBox1System", "comment": "VAV Serving HVAC Zone 1"},
    "properties": {
        ("supplyAirTemperature", Temperature): {},
    },
    "sensors": {
        ("SA-F", AirFlowSensor): {
            "hasUnit": UNIT["L-PER-SEC"],
            "comment": "Air flow used to control damper",
        },
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air supplied to zone by VAV 1, AKA discharge air temperature",
        },
        ("VAV1_ZN-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Zone Air Temperature Sensor (return of thermal mass zone 1)",
        },
        ("VAV1_ZN-H", AirHumiditySensor): {
            "comment": "Zone Air Humidity Sensor (return of thermal mass zone 1)",
        },
    },
    "equipment": {
        ("DPR", ElectricalActuatedProportionalDamper): {
            "comment": "VAV Box 1 Air Damper"
        },
        ("REHEAT", ElectricalHeatingCoil): {
            "comment": "VAV Box Electrical Heating Coil"
        },
    },
}

vav2_config = {
    "params": {"label": "VAVBox2System", "comment": "VAV Serving HVAC Zone 2"},
    "properties": {
        ("supplyAirTemperature", Temperature): {},
    },
    "sensors": {
        ("SA-F", AirFlowSensor): {
            "hasUnit": UNIT["L-PER-SEC"],
            "comment": "Air flow used to control damper",
        },
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air supplied to zone by VAV 2, AKA discharge air temperature",
        },
        ("VAV2_ZN-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Zone Air Temperature Sensor (return of thermal mass zone 2)",
        },
        ("VAV2_ZN-H", AirHumiditySensor): {
            "comment": "Zone Air Humidity Sensor (return of thermal mass zone 2)",
        },
    },
    "equipment": {
        ("DPR", ElectricalActuatedProportionalDamper): {
            "comment": "VAV Box 2 Air Damper"
        },
        ("REHEAT", ElectricalHeatingCoil): {
            "comment": "VAV Box Electrical Heating Coil"
        },
    },
}

vav3_config = {
    "params": {"label": "VAVBox3System", "comment": "VAV Serving HVAC Zone 3"},
    "properties": {
        ("supplyAirTemperature", Temperature): {},
    },
    "sensors": {
        ("SA-F", AirFlowSensor): {
            "hasUnit": UNIT["L-PER-SEC"],
            "comment": "Air flow used to control damper",
        },
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air supplied to zone by VAV 2, AKA discharge air temperature",
        },
        ("VAV3_ZN-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Zone Air Temperature Sensor (return of thermal mass zone 3)",
        },
        ("VAV3_ZN-H", AirHumiditySensor): {
            "comment": "Zone Air Humidity Sensor (return of thermal mass zone 3)",
        },
    },
    "equipment": {
        ("DPR", ElectricalActuatedProportionalDamper): {
            "comment": "VAV Box 3 Air Damper"
        },
        ("REHEAT", ElectricalHeatingCoil): {
            "comment": "VAV Box Electrical Heating Coil"
        },
    },
}

vav4_config = {
    "params": {"label": "VAVBox4System", "comment": "VAV Serving HVAC Zone 4"},
    "properties": {
        ("supplyAirTemperature", Temperature): {},
    },
    "sensors": {
        ("SA-F", AirFlowSensor): {
            "hasUnit": UNIT["L-PER-SEC"],
            "comment": "Air flow used to control damper",
        },
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air supplied to zone by VAV 2, AKA discharge air temperature",
        },
        ("VAV4_ZN-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Zone Air Temperature Sensor (return of thermal mass zone 4)",
        },
        ("VAV4_ZN-H", AirHumiditySensor): {
            "comment": "Zone Air Humidity Sensor (return of thermal mass zone 4)",
        },
    },
    "equipment": {
        ("DPR", ElectricalActuatedProportionalDamper): {
            "comment": "VAV Box 4 Air Damper"
        },
        ("REHEAT", ElectricalHeatingCoil): {
            "comment": "VAV Box Electrical Heating Coil"
        },
    },
}

fan_exhaust_template = {
    "cp": {
        "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
    },
    "params": {
        "hasRole": Role.Exhaust,
    },
}


ahu1 = AirHandlingUnit(config=ahu1_template)
ahu1["SF_VFD"] >> ahu1["SF"]
# ahu1["SF"].onOffStatus = ahu1["SF_VFD"].onOffStatus
# ahu1_clg_vlv = ThreeWayDivertingActuatedProportionalValve(label="valve1")

ahu2 = AirHandlingUnit(config=ahu2_template)
ahu2["SF_VFD"] >> ahu2["SF"]
# ahu2["SF"].onOffStatus = ahu1["SF_VFD"].onOffStatus
# ahu2_clg_vlv = ThreeWayDivertingActuatedProportionalValve(label="valve2")

ahu3 = AirHandlingUnit(config=ahu3_template)
ahu3["SF_Starter"] >> ahu3["SF"]
ahu3["SF"].onOffStatus = ahu3["SF_Starter"].onOffStatus

fan3 = Fan(
    config=fan_exhaust_template,
    label="ExhaustFan3",
    comment="Exhaust Fan 3",
)
fan3_vfd = VFD(label="FAN3_VFD")
fan3_vfd >> fan3

fan3_in_rtd = AirTemperatureSensor(label="fan3_in_rtd", hasUnit=UNIT.DEG_C)
fan3_in_flow = AirFlowSensor(label="fan3_in_flow")
fan3_in_pressure = AirDifferentialStaticPressureSensor(
    label="fan3_in_pressure", hasUnit=UNIT.PA
)
fan3_barometric_damper = GravityDamper(label="fan3_barometric_damper")

fan4 = Fan(
    config=fan_exhaust_template,
    label="ExhaustFan4",
    comment="Exhaust Fan 4",
)
fan4_vfd = VFD(label="FAN3_VFD")
fan4_vfd >> fan4
fan4_in_rtd = AirTemperatureSensor(label="fan4_in_rtd", hasUnit=UNIT.DEG_C)
fan4_in_flow = AirFlowSensor(label="fan4_in_flow")
fan4_in_pressure = AirDifferentialStaticPressureSensor(
    label="fan4_in_pressure", hasUnit=UNIT.PA
)
fan4_barometric_damper = GravityDamper(label="fan3_barometric_damper")

damper6 = ElectricalActuatedProportionalDamper(label="damper6")
damper8 = ElectricalActuatedProportionalDamper(label="damper8")
damper10 = ElectricalActuatedProportionalDamper(label="damper10")
damper15 = ElectricalActuatedProportionalDamper(label="damper15")
damper16 = ElectricalActuatedProportionalDamper(label="damper16")

# would need a bidirectional damper here....
damper5a = ElectricalActuatedProportionalDamper(
    label="damper5a", comment="from top to bottom"
)
damper5b = ElectricalActuatedProportionalDamper(
    label="damper5b", comment="from boottom to top"
)

damper10a = ElectricalActuatedProportionalDamper(
    label="damper10a", comment="from top to bottom"
)
damper10b = ElectricalActuatedProportionalDamper(
    label="damper10b", comment="from boottom to top"
)

outdoor_temp = AirTemperatureSensor(label="outdoor_temp", hasUnit=UNIT.DEG_C)
outdoor_hum = AirHumiditySensor(label="outdoor_hum")
outdoor_pressure = AirDifferentialStaticPressureSensor(
    label="outdoor_pressure", hasUnit=UNIT.PA
)

chiller1 = Chiller(label="Chiller1")
chilled_water_pump1 = Pump(label="ChilledWaterPump1")
chilled_water_pump1_starter = MotorStarter(label="ChilledWaterPump1Starter")
chilled_water_pump1_starter >> chilled_water_pump1

chiller2 = Chiller(label="Chiller2")
chilled_water_pump2 = Pump(label="ChilledWaterPump2")
chilled_water_pump2_starter = MotorStarter(label="ChilledWaterPump2Starter")
chilled_water_pump2_starter >> chilled_water_pump2

vav1 = VAV_Reheat(config=vav1_config, reheat_type="electrical")
vav2 = VAV_Reheat(config=vav2_config, reheat_type="electrical")
vav3 = VAV_Reheat(config=vav3_config, reheat_type="electrical")
vav4 = VAV_Reheat(config=vav4_config, reheat_type="electrical")


if __name__ == "__main__":
    dump()
