from bob.core import bind_model_namespace, dump, turtle
from bob.devices.boiler import (
    HotWaterBoiler,
    ElectricalHotWaterBoiler,
    NaturalGasHotWaterBoiler,
)
from bob.devices.coil import HotWaterCoil, ChilledWaterCoil, ElectricalHeatingCoil

__namespace__ = bind_model_namespace("ex", "urn:ex/")


def test_create_boilers():
    boiler = HotWaterBoiler(label="Boiler #1")
    electrical_hot_water_boiler = ElectricalHotWaterBoiler(label="Boiler #2")
    naturalgas_hot_water_boiler = NaturalGasHotWaterBoiler(label="Boiler #3")


def test_create_coils():
    hot_water_coil = HotWaterCoil(label="Coil #1")
    chilled_water_coil = ChilledWaterCoil(label="Coil #2")
    electrical_heating_coil = ElectricalHeatingCoil(label="Coil #3")


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    test_create_boilers()
    test_create_coils()
    result = turtle()
    with open("test_device-002_results.txt", "w") as file:
        file.write(result)
    print("Check file : test_device-002_results.ttl")
    print(result)
