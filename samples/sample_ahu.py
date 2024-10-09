from pathlib import Path

from bob.scratch.header import sample_header

from bob.connections.electricity import (
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from bob.core import UNIT, Role, bind_model_namespace, data_graph, dump, schema_graph

from bob.equipment.hvac.airhandlingunit import AirHandlingUnit
from bob.equipment.hvac.coil import ChilledWaterCoil, HotWaterCoil


from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.stats import AirDifferentialStaticPressureSensor
from bob.sensor.temperature import AirTemperatureSensor

# Prototypes
from bob.scratch.electricity.starter import MotorStarter_600VLL_3Ph_60Hz as MotorStarter
from bob.scratch.electricity.vfd import VFD
from bob.scratch.hvac.fan import Fan
from bob.scratch.hvac.damper import ElectricalActuatedProportionalDamper

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


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

ahu = AirHandlingUnit(config=ahu_template)
ahu["SF_Starter"] >> ahu["SF"]
ahu["RF_VFD"] >> ahu["RF"]

dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name, "data"),
)
dump(
    schema_graph,
    filename=f"samples/ttl/{model_name}.schema.ttl",
    header=sample_header(model_name, "schema"),
)
