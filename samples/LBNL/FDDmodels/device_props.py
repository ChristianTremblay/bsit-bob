"""
Dual Duct AHU
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from header import lbnl_header
from rdflib import URIRef

from bob.connections.air import (
    AirConnection,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.electricity import (
    Electricity_600V_3Ph_60HzInletConnectionPoint,
    Electricity_600V_3Ph_60HzOutletConnectionPoint,
)
from bob.core import *
from bob.equipment.archives.coolingcoil import ChilledWaterCoil2
from bob.equipment.archives.heatingcoil import HotWaterCoil2
from bob.equipment.hvac.damper import Damper
from bob.equipment.hvac.fan import Fan
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.vfd import VFD
from bob.externalreference.timeseries import TimeSeriesReference
from bob.properties.electricity import ElectricPowerW
from bob.properties.ratio import PercentAngularVelocity
from bob.property import QuantifiableObservableProperty, Setpoint
from bob.sensor.flow import AirFlowSensor
from bob.sensor.humidity import AirHumiditySensor
from bob.sensor.pressure import (
    AirDifferentialStaticPressureSensor,
    DifferentialStaticPressureSensor,
)
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSetpoint

# not sure of the difference between differential pressure and differential static pressure in this case


# not sure of the difference between differential pressure and differential static pressure in this case


model_name = Path(__file__).stem

_namespace = ex = bind_model_namespace(
    "LBNL", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

# add properties to config?
# Equipment DON'T have properties as default, but have a default config that you can optionally use.

# ddahu_fan_config = {
#     "sensors": {
#      ("Fan Speed", ): {
#                 "comment": "Supply Air Temperature sensor"
#             },
# }

# fan_template = {
#     "params": {
#         "label": "MyFan",
#         "comment": "A Big Fan",
#         "electricalInlet": Electricity_600V_3Ph_60HzInletConnectionPoint,
#         # "amps": 10,
#         # "rpm": 1770,
#         "powerFactor": 1.4,
#     },
#     "sensors": {
#         ("TPD1", AirDifferentialStaticPressureSensor): {
#             "comment": "Filter Differential Pressure Sensor"
#         },
#     },
#     "contains": {},
# }

# vfd_template = {
#     "params": {
#         "label": "MyVFD",
#         "comment": "A VFD for a Big Fan",
#         "electricalInlet": Electricity_600V_3Ph_60HzInletConnectionPoint,
#         "electricalOutlet": Electricity_600V_3Ph_60HzOutletConnectionPoint,
#         # "amps": 10,
#         # "hp": 10,
#     },
#     "sensors": {},
#     "contains": {},
# }

# DDAHU_Fan = Fan(config=fan_template)
# DDAHU_VFD = VFD(config=vfd_template)
# DDAHU_Fan > DDAHU_VFD  # include VFD in Fan
# DDAHU_VFD >> DDAHU_Fan  # connect electricity

# watt_ext_ref = ElectricPowerW()
# ext_ref1= TimeSeriesReference()
# watt_ext_ref.hasExternalReference  = ext_ref1
# DDAHU_Fan.W = watt_ext_ref

# f1  = Fan(label = 'f1',config=fan_template)
# f2  = Fan(label = 'f2')

# f3  = Fan(label = 'f3')
# f4 = Fan(label = 'f4')

# a = AirConnection()

# # f1>>a
# # f2>>a
# # a>>f3
# f3>>a>>f4
# f1>>a>>f2
s = PhysicalSpace(label="s")
a = DomainSpace(label="a")
z = Zone(label="z")
z.hasDomain = HVAC
z > a
s > a

lbnl_header(model_name)
dump()
