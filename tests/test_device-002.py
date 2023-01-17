from pathlib import Path

from header import ttl_test_header

from bob.core import bind_model_namespace, dump
from bob.equipment.hvac.boiler import (
    ElectricalHotWaterBoiler,
    HotWaterBoiler,
    NaturalGasHotWaterBoiler,
)
from bob.equipment.hvac.coil import (
    ChilledWaterCoil,
    ElectricalHeatingCoil,
    HotWaterCoil,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_more_complex_Equipments(bob_fixture):

    boiler = HotWaterBoiler(label="HWB-1", comment="Hot Water Boiler")
    electrical_hot_water_boiler = ElectricalHotWaterBoiler(
        label="Electrical Hot Water Boiler"
    )
    naturalgas_hot_water_boiler = NaturalGasHotWaterBoiler(
        label="HWB-2", comment="Natural Gas Hot Water Boiler"
    )

    hot_water_coil = HotWaterCoil(label="Hot Water Coil")
    chilled_water_coil = ChilledWaterCoil(label="Chilled Water Coil")
    electrical_heating_coil = ElectricalHeatingCoil(label="Electrical Heating Coil")

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
