"""
Figure A-10
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from header import g36_header

from bob.connections.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.electricity import (
    ModulationSignalInletConnectionPoint,
    OnOffSignalInletConnectionPoint,
    RS485BidirectionalConnectionPoint,
)
from bob.connections.water import (
    ChilledWaterConnection,
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterConnection,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
)
from bob.core import (
    Device,
    PropertyReference,
    System,
    bind_model_namespace,
    dump,
    quantitykind,
    unit,
)
from bob.devices.hvac.actuator import ElectricalProportionalActuator
from bob.devices.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.devices.hvac.damper import ElectricalActuatedProportionalDamper
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.gas import GasMonitor
from bob.devices.hvac.stats import (
    HighStaticPressureStat,
    NetworkRoomSensor,
    NetworkThermostat,
)
from bob.devices.hvac.valve import TwoWayActuatedProportionalValve, TwoWayValve
from bob.devices.hvac.vfd import VFD
from bob.functions.g36 import AnalogIn, AnalogOut, BinaryIn, G36Sequence
from bob.properties import Flow, PercentCommand, Temperature
from bob.properties.states import SmokePresence
from bob.properties.volume import Gallons
from bob.property import QuantifiableObservableProperty
from bob.sensor.fire import SmokeDetectionSensor
from bob.sensor.flow import AirFlowSensor
from bob.sensor.gas import CO2Sensor
from bob.sensor.movement import IntrusionSensor, OccupancySensor
from bob.sensor.pressure import DifferentialStaticPressureSensor
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSetpoint
from bob.space.hvac import HVACSpace

model_name = Path(__file__).stem
_namespace = bind_model_namespace(
    "exg3610", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

min_oa_dpr = ElectricalActuatedProportionalDamper(
    label="MIN-OA-DPR", comment="Minimum ouside air damper, 2 pos"
)
econ_dpr = ElectricalActuatedProportionalDamper(
    label="ECON-DPR", comment="Economizer damper, modulating"
)

outside = AirConnection(label="Outside")
mixed_air_supply = AirConnection(label="MixedAirSupply")
oat = AirTemperatureSensor(label="OA-T", unit=unit.DEG_C, comment="Outside Air Temp")
mat = AirTemperatureSensor(label="MA-T", unit=unit.DEG_C, comment="Mixed Air Temp")

filter = Filter(label="Filter")
filter_dpt = DifferentialStaticPressureSensor(
    label="DPT-1", unit=unit.PA, comment="Filter Differential Pressure Transmitter"
)

# Heating coil
hot_water_valve_template = {
    "cp": {
        "waterInlet": HotWaterInletConnectionPoint,
        "waterOutlet": HotWaterOutletConnectionPoint,
        "positionInlet": ModulationSignalInletConnectionPoint,
        "onOffInlet": OnOffSignalInletConnectionPoint,
    },
    "properties": {
        ("flowCoefficient", Gallons): {},
    },
    "devices": {("actuator", ElectricalProportionalActuator): {}},
}
htg_coil = HotWaterCoil(label="HWC", comment="Hot Water Coil")
htg_vlv = TwoWayActuatedProportionalValve(
    label="HTG-VLV", comment="Heating 2W Valve", config=hot_water_valve_template
)
hwct = AirTemperatureSensor(
    label="HTGCOIL-T", unit=unit.DEG_C, comment="Heat Coil Air Temp"
)

hws = HotWaterConnection(label="Hot Water Supply")
hwr = HotWaterConnection(label="Hot Water Return")

# Cooling Coil
chilled_water_valve_template = {
    "cp": {
        "waterInlet": ChilledWaterInletConnectionPoint,
        "waterOutlet": ChilledWaterOutletConnectionPoint,
        "positionInlet": ModulationSignalInletConnectionPoint,
        "onOffInlet": OnOffSignalInletConnectionPoint,
    },
    "properties": {
        ("flowCoefficient", Gallons): {},
    },
    "devices": {("actuator", ElectricalProportionalActuator): {}},
}
clg_coil = ChilledWaterCoil(label="CWC", comment="Chilled Water Coil")
clg_vlv = TwoWayActuatedProportionalValve(
    label="CLG-VLV", comment="Cooling 2W Valve", config=chilled_water_valve_template
)

chws = ChilledWaterConnection(label="Chilled Water Supply")
chwr = ChilledWaterConnection(label="Chilled Water Return")

# Supply Fan with its VFD
sf = Fan(label="SF", comment="Supply Fan")
sf_vfd = VFD(label="SF-VFD", comment="Supply Fan VFD")


# Protections
hsp_limit_mix = HighStaticPressureStat(label="HighStaticPressureLimit_Mix")
hsp_limit_supply = HighStaticPressureStat(label="HighStaticPressureLimit_Supply")
smoke = SmokeDetectionSensor(label="SD", comment="Supply Air Smoke Detector")

sat = AirTemperatureSensor(label="SA-T", unit=unit.DEG_C, comment="Supply Air Temp")
duct_dpt = DifferentialStaticPressureSensor(
    label="DPT-2", unit=unit.PA, comment="Duct Static Pressure Transmitter"
)

supply_air = AirConnection(label="Supply Air")
return_air = AirConnection(label="Return Air")

rat = AirTemperatureSensor(label="RA-T", unit=unit.DEG_C, comment="Return Air Temp")

rad = ElectricalActuatedProportionalDamper(label="RAD", comment="Return Air Damper")

# Exhaust Fan with its VFD
ef = Fan(label="EF", comment="Exhaust Fan")
ef_vfd = VFD(label="EF-VFD", comment="Exhaust Fan VFD")
ead = ElectricalActuatedProportionalDamper(label="EAD", comment="Exhaust Air Damper")

building_dpt = DifferentialStaticPressureSensor(
    label="DPT-3", unit=unit.PA, comment="Building Static Pressure Transmitter"
)

hvacspace = HVACSpace(label="SPACE", comment="Space where this unit feeds air")

# Connections
# AIR
outside >> min_oa_dpr >> mixed_air_supply
outside >> econ_dpr >> mixed_air_supply
rad.airOutlet >> mixed_air_supply

mixed_air_supply >> filter >> htg_coil >> clg_coil >> sf >> supply_air >> hvacspace.ductAirInlet
hvacspace.ductAirOutlet >> return_air
return_air >> ef.airInlet
ef >> ead >> outside
return_air >> rad.airInlet

# WATER
hws >> htg_coil.hotWaterInlet
### TODO htg_coil.hotWaterOutlet >> htg_vlv >> hwr

chws >> clg_coil.chilledWaterInlet
### TODO clg_coil.chilledWaterOutlet >> clg_vlv >> chwr

# Sensors measurements
oat.hasMeasurementLocation = econ_dpr.airOutlet
hsp_limit_mix["pressure_sensor"].hasMeasurementLocationHigh = hvacspace
hsp_limit_mix["pressure_sensor"].hasMeasurementLocationLow = mixed_air_supply
mat.hasMeasurementLocation = mixed_air_supply
filter_dpt.hasMeasurementLocationHigh = filter.airInlet
filter_dpt.hasMeasurementLocationLow = filter.airOutlet
hwct.hasMeasurementLocation = htg_coil.airOutlet
hsp_limit_supply["pressure_sensor"].hasMeasurementLocationLow = hvacspace
hsp_limit_supply["pressure_sensor"].hasMeasurementLocationHigh = sf.airOutlet
smoke.hasMeasurementLocation = supply_air
sat.hasMeasurementLocation = supply_air
duct_dpt.hasMeasurementLocationHigh = supply_air
duct_dpt.hasMeasurementLocationLow = hvacspace
building_dpt.hasMeasurementLocationHigh = hvacspace
building_dpt.hasMeasurementLocationLow = outside


class G36_FIG10_AHU(System):
    returnAir: AirInletSystemConnectionPoint
    supplyAir: AirOutletSystemConnectionPoint
    exhaustAir: AirOutletSystemConnectionPoint
    outdoorAir: AirInletSystemConnectionPoint
    cooling: PropertyReference
    heating: PropertyReference
    return_air_temp: PropertyReference
    supply_air_temp: PropertyReference


ahu = G36_FIG10_AHU(label="AHU", comment="Is this really required ?")
ahu.returnAir.mapsTo = return_air
ahu.supplyAir.mapsTo = supply_air
ahu.exhaustAir.mapsTo = ead.airOutlet
ahu.outdoorAir.mapsTo = econ_dpr.airInlet
ahu.cooling = clg_vlv.position  #
ahu.heating = htg_vlv.position  # equivalent to htg_vlv['actuator']['postion']


# TODO : Complete this
# Definition of G36
sequence = "lorem ipsum of sequence"
g36_fig_a_10 = G36Sequence(label="G36_FIG_A_10", comment=sequence)

g36_fig_a_10.uses_input(rat.observesProperty, AnalogIn, "return-air-temp")
g36_fig_a_10.produces_output(htg_vlv["actuator"]["command"], AnalogOut, "HW VALVE")

dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
