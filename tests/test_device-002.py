from bob.core import bind_model_namespace, dump
from bob.devices.hvac.boiler import (
    HotWaterBoiler,
    ElectricalHotWaterBoiler,
    NaturalGasHotWaterBoiler,
)
from bob.devices.hvac.coil import HotWaterCoil, ChilledWaterCoil, ElectricalHeatingCoil

from pathlib import Path

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


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

dump()
