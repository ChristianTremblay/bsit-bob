from pathlib import Path



from bob.connections.electricity import (
    Electricity_120VLN_1Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from bob.core import UNIT, Role, bind_model_namespace, dump
from bob.equipment.architectural import Window
from bob.equipment.electricity.starter import MotorStarter
from bob.equipment.electricity.vfd import VFD
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
from bob.equipment.hvac.fan import Fan
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

from bob.bacnet import Device

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


vav1_config = {
    "params": {"label": "vav1", "comment": "VAV Serving HVAC Zone 1"},
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
        ("ZN-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Zone Air Temperature Sensor (return of thermal mass zone 1)",
        },
        ("ZN-H", AirHumiditySensor): {
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

class BACnetVAV(VAV_Reheat, Device):
    pass

vav1 = BACnetVAV(config=vav1_config)



if __name__ == "__main__":
    dump()
