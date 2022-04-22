"""
Dual Duct AHU
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from header import lbnl_header

from bob.connections.air import (
    AirConnection,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.electricity import (
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
)
from bob.core import Junction, System, bind_model_namespace, dump, quantitykind, unit
from bob.devices.hvac.damper import Damper
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.vfd import VFD
from bob.property import QuantifiableObservableProperty
from bob.sensor.flow import AirFlowSensor
from bob.sensor.humidity import AirHumiditySensor
from bob.sensor.pressure import AirDifferentialStaticPressureSensor
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSetpoint
from bob.systems.archives.coolingcoil import ChilledWaterCoil2
from bob.systems.archives.heatingcoil import HotWaterCoil2

# not sure of the difference between differential pressure and differential static pressure in this case


model_name = Path(__file__).stem
_namespace = ex = bind_model_namespace(
    "ex", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

# add properties to config?
# Devices DON'T have properties as default, but have a default config that you can optionally use.

# ddahu_fan_config = {
#     "sensors": {
#      ("Fan Speed", ): {
#                 "comment": "Supply Air Temperature sensor"
#             },
# }


fan_template = {
    "params": {
        "label": "MyFan",
        "comment": "A Big Fan",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "amps": 10,
        "hp": 10,
        "rpm": 1770,
        "powerFactor": 1.4,
    },
    "sensors": {},
    "devices": {},
}

vfd_template = {
    "params": {
        "label": "MyVFD",
        "comment": "A VFD for a Big Fan",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
        "amps": 10,
        "hp": 10,
    },
    "sensors": {},
    "devices": {},
}

DDAHU_Fan = Fan(config=fan_template)
DDAHU_VFD = VFD(config=vfd_template)
DDAHU_Fan > DDAHU_VFD  # include VFD in Fan
DDAHU_VFD >> DDAHU_Fan  # connect electricity

# probably just need 1 subclass for deck
class HotDeck(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        in_filter = Filter(label=self.label + ".filter")
        self.airInlet.mapsTo = in_filter.airInlet
        hwc = HotWaterCoil2(
            label=self.label + ".hot_water_coil"
        )  # may have to add some measurement points to this.
        hsf = Fan(label=self.label + ".hot_supply_fan")
        self.airOutlet.mapsTo = hsf.airOutlet
        in_filter >> hwc >> hsf

        hsf_dp = AirDifferentialStaticPressureSensor(
            label=self.label + ".fan_dp_sensor"
        )
        hsf_dp.hasMeasurementLocationHigh = hsf.airOutlet
        hsf_dp.hasMeasurementLocationLow = hsf.airInlet
        # more sensors
        dat = AirTemperatureSensor(label=self.label + ".discharge_air_temp_sensor")
        humd = AirHumiditySensor(label=self.label + ".air_humidity_sensor")
        cfm = AirFlowSensor(label=self.label + ".air_flow_sensor")
        temp = AirTemperatureSensor(label=self.label + ".air_temp_sensor")

        temp_sp = TemperatureSetpoint(label=self.label + ".air_temp_setpoint")
        temp.observesProperty.hasSetpoint = temp_sp

        dat.hasMeasurementLocation = hwc.airOutlet
        humd.hasMeasurementLocation = hsf.airOutlet
        cfm.hasMeasurementLocation = hsf.airOutlet
        temp.hasMeasurementLocation = hsf.airOutlet


class ColdDeck(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        in_filter = Filter(label=self.label + ".filter")
        self.airInlet.mapsTo = in_filter.airInlet
        hwc = HotWaterCoil2(label=self.label + ".cold_water_coil")
        hsf = Fan(label=self.label + ".cold_supply_fan")
        self.airOutlet.mapsTo = hsf.airOutlet
        in_filter >> hwc >> hsf

        hsf_dp = AirDifferentialStaticPressureSensor(
            label=self.label + ".fan_dp_sensor"
        )
        hsf_dp.hasMeasurementLocationHigh = hsf.airOutlet
        hsf_dp.hasMeasurementLocationLow = hsf.airInlet
        # more sensors
        dat = AirTemperatureSensor(label=self.label + ".discharge_air_temp_sensor")
        humd = AirHumiditySensor(label=self.label + ".air_humidity_sensor")
        cfm = AirFlowSensor(label=self.label + ".air_flow_sensor")
        temp = AirTemperatureSensor(label=self.label + ".air_temp_sensor")

        temp_sp = TemperatureSetpoint(label=self.label + ".air_temp_setpoint")
        temp.observesProperty.hasSetpoint = temp_sp

        dat.hasMeasurementLocation = hwc.airOutlet
        humd.hasMeasurementLocation = hsf.airOutlet
        cfm.hasMeasurementLocation = hsf.airOutlet
        temp.hasMeasurementLocation = hsf.airOutlet


class DDAHU(System):
    outsideAirInlet: AirInletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    supplyHotAirOutlet: AirOutletSystemConnectionPoint
    supplyColdAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        oa_damper = Damper(label=self.label + ".oa_damper")

        oa_dat = AirTemperatureSensor(label=self.label + ".oa_air_temp_sensor")
        oa_humd = AirHumiditySensor(label=self.label + ".oa_air_humidity_sensor")
        oa_cfm = AirFlowSensor(label=self.label + ".oa_air_flow_sensor")
        # could put function for the above sensors

        oa_dat.hasMeasurementLocation = oa_damper.airInlet
        oa_humd.hasMeasurementLocation = oa_damper.airInlet
        oa_cfm.hasMeasurementLocation = oa_damper.airInlet

        self.outsideAirInlet.mapsTo = oa_damper.airInlet
        # sensors attach here

        mixed_air = AirConnection(label=self.label + ".mixed_air")
        oa_damper >> mixed_air
        ma_temp = AirTemperatureSensor(label=self.label + "ma_air_temp_sensor")
        ma_temp.hasMeasurementLocation = mixed_air

        return_air_fan = Fan(label=self.label + ".return_air_fan")
        self.returnAirInlet.mapsTo = return_air_fan.airInlet

        re_dat = AirTemperatureSensor(label=self.label + ".re_air_temp_sensor")
        re_humd = AirHumiditySensor(label=self.label + ".re_air_humidity_sensor")
        re_cfm = AirFlowSensor(label=self.label + ".re_air_flow_sensor")

        re_dat.hasMeasurementLocation = return_air_fan.airInlet
        re_humd.hasMeasurementLocation = return_air_fan.airInlet
        re_cfm.hasMeasurementLocation = return_air_fan.airInlet
        # sensors here and about fan

        j1 = Junction()
        j1.link_to(return_air_fan.airOutlet)

        recirc_damper = Damper(label=self.label + ".recirculated_air_damper")
        exhaust_damper = Damper(label=self.label + ".exhaust_damper")

        j1.link_to(recirc_damper.airInlet)
        j1.link_to(exhaust_damper.airInlet)

        self.exhaustAirOutlet.mapsTo = exhaust_damper.airOutlet

        recirc_damper >> mixed_air

        hot_deck = HotDeck(label=self.label + ".hot_deck")
        mixed_air >> hot_deck.airInlet

        cold_deck = ColdDeck(label=self.label + ".cold_deck")
        mixed_air >> cold_deck

        self.supplyColdAirOutlet.mapsTo = cold_deck.airOutlet
        self.supplyHotAirOutlet.mapsTo = hot_deck.airOutlet


ddahu = DDAHU(label="DDAHU")
# vfd = VFD(label = 'vfd', properties = {'Electric_Power': Electric_Power})
# vfd.properties['Electric_Power'].hasSetpoint = ep
lbnl_header(model_name)
dump()
