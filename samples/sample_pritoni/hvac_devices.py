from pathlib import Path
from bob.devices.hvac.pump import PumpWithStarter
from bob.devices.hvac.valve import TwoWayActuatedProportionalValve

import hvac_spaces as hs
import physical_spaces as ps

from bob.connections.electricity import (
    Electricity_120V_60HzInletConnectionPoint,
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
    EthernetBidirectionalConnectionPoint,
)
from bob.core import bind_model_namespace, dump, UNIT, Role
from bob.devices.architectural import Window
from bob.devices.electricity.starter import MotorStarter
from bob.devices.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.devices.hvac.damper import ElectricalActuatedProportionalDamper
from bob.devices.hvac.fan import Fan, FanWithStarter, FanWithVFD
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.stats import AirDifferentialStaticPressureSensor
from bob.devices.hvac.chiller import Chiller
from bob.devices.hvac.boiler import ElectricalHotWaterBoiler
from bob.devices.electricity.vfd import VFD
from bob.sensor.flow import AirFlowSensor
from bob.sensor.pressure import DifferentialStaticPressure
from bob.sensor.temperature import AirTemperatureSensor, Temperature
from bob.systems.hvac.airhandlingunit import AirHandlingUnit
from bob.systems.hvac.vav import VAV

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


ahu_template = {
    "params": {"label": "AHU", "comment": "AHU delivering air to 2 VAV boxes"},
    "sensors": {
        ("OA-T", AirTemperatureSensor): {
            "unit": UNIT.DEG_C,
            "comment": "Oudoor air temperature (S3)",
        },
        ("TPD1", AirDifferentialStaticPressureSensor): {
            "unit": UNIT.PA,
            "comment": "Filter Differential Pressure Sensor (S5)",
        },
        ("HC-T", AirTemperatureSensor): {
            "unit": UNIT.DEG_C,
            "comment": "Air temperature after heating coil (S6)",
        },
        ("MA-T", AirTemperatureSensor): {
            "unit": UNIT.DEG_F,
            "comment": "Return Air temperature (S4)",
        },
        ("DA-T", AirTemperatureSensor): {
            "unit": UNIT.DEG_F,
            "comment": "Discharge Air temperature after cooling coil (S7)",
        },
        ("RA-T", AirTemperatureSensor): {
            "unit": UNIT.DEG_F,
            "comment": "Return Air temperature (S2)",
        },
        ("TPD2", AirDifferentialStaticPressureSensor): {
            "unit": UNIT.PA,
            "comment": "Supply Duct Static Pressure (S8)",
        },
        ("TPD3", AirDifferentialStaticPressureSensor): {
            "unit": UNIT.PA,
            "comment": "Return Duct Static Pressure (S1)",
        },
    },
    "devices": {
        ("RF", FanWithVFD): {
            "comment": "Return Air Fan",
            "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
            "hasRole": Role.Return,
        },
        ("SF", FanWithStarter): {
            "comment": "Supply Air Fan",
            "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
            "hasRole": Role.Supply,
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
    "sensors": {
        ("VAV1_SA-F", AirFlowSensor): {
            "unit": UNIT["L-PER-SEC"],
            "comment": "Air flow used to control damper (S9)",
        },
        ("VAV1_DA-T", AirTemperatureSensor): {
            "unit": UNIT.DEG_F,
            "comment": "Air supplied to zone by VAV 1, AKA discharge air temperature (S10)",
        },
        ("VAV1_ZN-T", AirTemperatureSensor): {
            "unit": UNIT.DEG_F,
            "comment": "Zone Air Temperature Sensor, which is a thermostats...",
        },
    },
    "devices": {
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
    "sensors": {
        ("VAV2_SA-F", AirFlowSensor): {
            "unit": UNIT["L-PER-SEC"],
            "comment": "Air flow used to control damper (S11)",
        },
        ("VAV2_DA-T", AirTemperatureSensor): {
            "unit": UNIT.DEG_F,
            "comment": "Air supplied to zone by VAV 2, AKA discharge air temperature (S12)",
        },
        ("VAV2_ZN-T", AirTemperatureSensor): {
            "unit": UNIT.DEG_F,
            "comment": "Zone Air Temperature Sensor, which is a thermostats...",
        },
    },
    "devices": {
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

chiller = Chiller(label="Chiller")
chilled_water_pump = PumpWithStarter(label="ChilledWaterPump")
boiler = ElectricalHotWaterBoiler(label="Boiler")
hot_water_pump = PumpWithStarter(label="HotWaterPump")


exhaustfan_template = {
    "cp": {
        "electricalInlet": Electricity_120V_60HzInletConnectionPoint,
    },
    "params":{
        "hasRole": Role.Exhaust,
    }
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
vav1.serves_zone(hs.hvac_zone_1)
vav2 = VAV(config=vav2_config)
vav2.serves_zone(hs.hvac_zone_2)


if __name__ == "__main__":
    dump()
