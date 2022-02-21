from bob.core import bind_model_namespace, dump, turtle, get_datagraph
from bob.devices.hvac.boiler import (
    HotWaterBoiler,
    ElectricalHotWaterBoiler,
    NaturalGasHotWaterBoiler,
)
from bob.devices.hvac.coil import HotWaterCoil, ChilledWaterCoil, ElectricalHeatingCoil

from pathlib import Path

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_boilers():
    boiler = HotWaterBoiler(label="HWB-1", comment="Hot Water Boiler")
    electrical_hot_water_boiler = ElectricalHotWaterBoiler(
        label="Electrical Hot Water Boiler"
    )
    naturalgas_hot_water_boiler = NaturalGasHotWaterBoiler(
        label="HWB-2", comment="Natural Gas Hot Water Boiler"
    )


def test_create_coils():
    hot_water_coil = HotWaterCoil(label="Hot Water Coil")
    chilled_water_coil = ChilledWaterCoil(label="Chilled Water Coil")
    electrical_heating_coil = ElectricalHeatingCoil(label="Electrical Heating Coil")


def test_turtle_file():
    dump()
    result = turtle(filename=f"tests/ttl/{model_name}.ttl")
    print(result)
    return result


if __name__ == "__main__":
    test_create_boilers()
    test_create_coils()
    result = test_turtle_file()
    print(f"Check file : tests/ttl/{model_name}.ttl")
    print(result)
    graph = get_datagraph()  # this is there to be used with python -i option
