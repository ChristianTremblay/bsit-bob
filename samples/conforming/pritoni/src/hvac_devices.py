from pathlib import Path

import hvac_spaces as hs
import physical_spaces as ps

from bob.connections.air import AirConnection
from bob.connections.electricity import (
    Electricity_120VLN_1Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from bob.core import UNIT, Role, bind_model_namespace, dump
from bob.equipment.architectural import Window
from bob.equipment.hvac.airhandlingunit import AirHandlingUnit
from bob.equipment.hvac.boiler import ElectricalHotWaterBoiler
from bob.equipment.hvac.chiller import Chiller
from bob.equipment.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.heatexchanger import AirHeatExchanger
from bob.equipment.hvac.pump import Pump, PumpWithStarter
from bob.equipment.hvac.stats import AirDifferentialStaticPressureSensor

# Prototypes
from bob.scratch.electricity.starter import MotorStarter_600VLL_3Ph_60Hz as MotorStarter
from bob.scratch.electricity.vfd import VFD
from bob.scratch.hvac.damper import ElectricalActuatedProportionalDamper
from bob.scratch.hvac.fan import Fan
from bob.scratch.hvac.valve import TwoWayActuatedProportionalValve
from bob.scratch.hvac.vav import VAV
from bob.sensor.flow import AirFlowSensor
from bob.sensor.pressure import DifferentialStaticPressure
from bob.sensor.temperature import AirTemperatureSensor, Temperature
from bob.assemblage import model_namespace

model_name, global_ns = model_namespace(__file__)
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


ahu_template = {
    "params": {"label": "AHU", "comment": "AHU delivering air to 2 VAV boxes"},
    "sensors": {
        ("OA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Oudoor air temperature (S3)",
        },
        ("TPD1", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Filter Differential Pressure Sensor (S5)",
        },
        ("HC-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after heating coil (S6)",
        },
        ("MA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_F,
            "comment": "Return Air temperature (S4)",
        },
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_F,
            "comment": "Discharge Air temperature after cooling coil (S7)",
        },
        ("RA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_F,
            "comment": "Return Air temperature (S2)",
        },
        ("TPD2", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Supply Duct Static Pressure (S8)",
        },
        ("TPD3", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Return Duct Static Pressure (S1)",
        },
    },
    "equipment": {
        ("RF", Fan): {
            "comment": "Return Air Fan",
            "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            "hasRole": Role.Return,
        },
        ("RF_VFD", VFD): {
            "comment": "Return Air Fan VFD",
        },
        ("SF", Fan): {
            "comment": "Supply Air Fan",
            "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            "hasRole": Role.Supply,
        },
        ("SF_Starter", MotorStarter): {
            "comment": "Supply Air Fan Starter",
        },
        ("CLGCOIL", ChilledWaterCoil): {"comment": "Cooling Coil"},
        ("HTGCOIL", HotWaterCoil): {"comment": "Heating coil"},
        ("FILTER", Filter): {"comment": "Filter"},
        ("OADPR", ElectricalActuatedProportionalDamper): {
            "comment": "Outdoor air damper (A3)"
        },
        ("MADPR", ElectricalActuatedProportionalDamper): {
            "comment": "Mixed Air Damper (A2)"
        },
        ("EADPR", ElectricalActuatedProportionalDamper): {
            "comment": "Exhaust Air Damper (A1)"
        },
    },
}

vav1_config = {
    "params": {"label": "VAVBox1System", "comment": "VAV Serving HVAC Zone 1"},
    "sensors": {},
    "equipment": {
        ("VAV1_damper", ElectricalActuatedProportionalDamper): {
            "comment": "VAV Box 1 Air Damper (actuator:Ax)"
        },
        ("VAV1_HeatingCoil", HotWaterCoil): {
            "comment": "VAV Box 1 Hot Water Coil (actuator:Ay"
        },
    },
}

vav2_config = {
    "params": {"label": "VAVBox2System", "comment": "VAV Serving HVAC Zone 2"},
    "sensors": {},
    "equipment": {
        ("VAV2_damper", ElectricalActuatedProportionalDamper): {
            "comment": "VAV Box 2 Air Damper (actuator:A6)"
        },
        ("VAV2_HeatingCoil", HotWaterCoil): {
            "comment": "VAV Box 2 Hot Water Coil (actuator:A7)"
        },
    },
}

ahu = AirHandlingUnit(config=ahu_template)

clg_vlv = TwoWayActuatedProportionalValve(label="A5")
htg_vlv = TwoWayActuatedProportionalValve(label="A4")

hrv = AirHeatExchanger(label="HRV")

chiller = Chiller(label="Chiller")
chilled_water_pump = Pump(label="ChilledWaterPump")
chilled_water_pump_starter = MotorStarter(label="ChilledWaterPumpStarter")
chilled_water_pump_starter >> chilled_water_pump
boiler = ElectricalHotWaterBoiler(label="Boiler")
hot_water_pump = Pump(label="HotWaterPump")
hot_water_pump_starter = MotorStarter(label="HotWaterPumpStarter")
hot_water_pump_starter >> hot_water_pump


exhaustfan_template = {
    "cp": {
        "electricalInlet": Electricity_120VLN_1Ph_60HzInletConnectionPoint,
    },
    "params": {
        "hasRole": Role.Exhaust,
    },
}
bathroom_exhaust_fan = Fan(
    config=exhaustfan_template,
    label="ExhaustFan",
    comment="Bathroom exhaust fan",
    hasPhysicalLocation=ps.bathroom,
)
window1 = Window(
    label="Window_West",
    comment="First Window in OpenOffice, covering West portion of room",
)
window2 = Window(
    label="Window_East",
    comment="Second Window in OpenOffice, covering East portion of room",
)

vav1 = VAV(config=vav1_config)
vav2 = VAV(config=vav2_config)


if __name__ == "__main__":
    dump()
