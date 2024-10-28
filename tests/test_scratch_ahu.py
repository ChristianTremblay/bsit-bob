from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl, model_namespace
from bob.connections import AirConnection
from bob.connections.electricity import Electricity_600VLL_3Ph_60HzInletConnectionPoint
from bob.core import UNIT, Role, bind_model_namespace
from bob.equipment.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.stats import AirDifferentialStaticPressureSensor
from bob.scratch.electricity.starter import MotorStarter_600VLL_3Ph_60Hz as MotorStarter
from bob.scratch.electricity.vfd import VFD
from bob.scratch.header import sample_header
from bob.scratch.hvac.airhandlingunit import AirHandlingUnit
from bob.scratch.hvac.damper import ElectricalActuatedProportionalDamper
from bob.scratch.hvac.fan import Fan
from bob.sensor.temperature import AirTemperatureSensor

model_name, global_ns = model_namespace(__file__)
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}:{model_name}/")

ahu_template = {
    "params": {"label": "AHU", "comment": "AHU delivering air to 2 VAV boxes"},
    "sensors": {
        ("OA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Oudoor air temperature",
        },
        ("TPD1", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Filter Differential Pressure Sensor",
        },
        ("HC-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Air temperature after heating coil",
        },
        ("MA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_F,
            "comment": "Return Air temperature",
        },
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_F,
            "comment": "Discharge Air temperature after cooling coil",
        },
        ("RA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_F,
            "comment": "Return Air temperature",
        },
        ("TPD2", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Supply Duct Static Pressure",
        },
        ("TPD3", AirDifferentialStaticPressureSensor): {
            "hasUnit": UNIT.PA,
            "comment": "Return Duct Static Pressure",
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
            "comment": "Outdoor air damper"
        },
        ("MADPR", ElectricalActuatedProportionalDamper): {
            "comment": "Mixed Air Damper"
        },
        ("EADPR", ElectricalActuatedProportionalDamper): {
            "comment": "Exhaust Air Damper"
        },
    },
    "relations": [
        ("self['SF_Starter'].electricalOutlet", ">>", "self['SF'].electricalInlet"),
        ("self['RF_VFD'].electricalOutlet", ">>", "self['RF'].electricalInlet"),
        ('self["OADPR"].airOutlet', ">>", "self.mixedAir"),
        ('self["MADPR"].airOutlet', ">>", "self.mixedAir"),
        ("self.mixedAir", ">>", 'self["FILTER"].airInlet'),
        ('self["FILTER"].airOutlet', ">>", 'self["CLGCOIL"].airInlet'),
        ('self["CLGCOIL"].airOutlet', ">>", 'self["SF"].airInlet'),
        ('self["SF"].airOutlet', ">>", 'self["HTGCOIL"].airInlet'),
        ('self["HTGCOIL"].airOutlet', ">>", "self.supplyAir"),
        ("self.returnAir", ">>", 'self["RF"].airInlet'),
        ('self["RF"].airOutlet', ">>", "self.returnExhaust"),
        ("self.returnExhaust", ">>", 'self["EADPR"].airInlet'),
        ("self.returnExhaust", ">>", 'self["MADPR"].airInlet'),
        ('self["TPD1"]["highPort"]', "%", 'self["FILTER"].airInlet'),
        ('self["MA-T"]', "%", 'self["FILTER"].airInlet'),
        ('self["TPD1"]["lowPort"]', "%", 'self["FILTER"].airOutlet'),
        ('self["HC-T"]', "%", 'self["HTGCOIL"].airOutlet'),
        ('self["DA-T"]', "%", 'self["SF"].airOutlet'),
        ('self["RA-T"]', "%", 'self["MADPR"].airInlet'),
        ('self["TPD2"]["highPort"]', "%", 'self["SF"].airOutlet'),
        # ('self["TPD2"]["lowPort"]', "%", 'self.plenum'),
        ('self["TPD3"]["highPort"]', "%", 'self["RF"].airOutlet'),
        # ('self["TPD3"]["lowPort"]', "%", 'self.plenum'),
    ],
}

outdoor = AirConnection(
    label="Outdoor",
    comment="This is where we exhaust air of bathroom, and windows of OpenOffice are connected here to",
)
plenum = AirConnection(
    label="Plenum",
    comment="Plenum. It's where Duct Static Pressure Low port is connected",
)

ahu = AirHandlingUnit(config=ahu_template, label="ahu")

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
