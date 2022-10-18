"""
Dual Duct AHU

# dp in in. WG
# should hot air be its own medium?
# Filling external reference into config
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from header import lbnl_header

from bob.connections.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.electricity import (
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
)
from bob.core import (
    HVAC,
    QUANTITYKIND,
    UNIT,
    Air,
    Equipment,
    DomainSpace,
    Junction,
    System,
    bind_model_namespace,
    dump,
    p223,
)
from bob.equipments.archives.coolingcoil import ChilledWaterCoil2
from bob.equipments.archives.heatingcoil import HotWaterCoil2
from bob.equipments.electricity.vfd import VFD
from bob.equipments.hvac.damper import Damper
from bob.equipments.hvac.fan import Fan
from bob.equipments.hvac.filter import Filter
from bob.externalreference.timeseries import TimeSeriesReference
from bob.properties.electricity import ElectricPowerW
from bob.properties.ratio import PercentAngularVelocity
from bob.property import QuantifiableObservableProperty
from bob.sensor.flow import AirFlowSensor
from bob.sensor.humidity import AirHumiditySensor
from bob.sensor.pressure import AirDifferentialPressureSensor, AirStaticPressureSensor
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSetpoint

# not sure of the difference between differential pressure and differential static pressure in this case


# not sure of the difference between differential pressure and differential static pressure in this case


model_name = Path(__file__).stem
_namespace = ex = bind_model_namespace(
    "ex", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

# add properties to config?
# Equipments DON'T have properties as default, but have a default config that you can optionally use.

fan_template = {
    "params": {
        "label": "MyFan",
        "comment": "A Big Fan",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
    },  # Fans also have % Speed and On/Off status
    "sensors": {
        ("TPD1", AirDifferentialPressureSensor): {
            "comment": "Filter Differential Pressure Sensor"
        },
    },
    "equipments": {},
}

vfd_template = {
    "params": {
        "label": "MyVFD",
        "comment": "A VFD for a Big Fan",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
    },
    "sensors": {},
    "equipments": {},
}

# will need my own damper since this has no control point properties like g36
damper_template = {
    "params": {"label": "damper", "comment": "A hot or cold damper"},
    "sensors": {
        ("vav_eat", AirTemperatureSensor): {
            "comment": "Air Temperature Sensor",
            "hasExternalReference": TimeSeriesReference,
        },
        ("vav_cfm", AirFlowSensor): {},
        ("vav_dp", AirStaticPressureSensor): {},
    },
    "equipments": {},
}

mixing_box_template = {
    "params": {"label": "damper", "comment": "A hot or cold damper"},
    "sensors": {
        ("vav_eat", AirTemperatureSensor): {"comment": "Air Temperature Sensor"}
    },
    "equipments": {},
}


# don't need these functions in the future I think
def ext_ref_damper(label, ext_ref=None):
    dmp = Damper(label=label, config=damper_template)
    # able to specify in config if they attach at inlet, outlet, or Equipment?
    # not defining sensors in template, since I want to specify that they connect at inlet connection point?
    # defining sensors in template, then specifying here that they should measure inlet cp

    # dmp['vav_dp'].hasExternalReference = TimeSeriesReference
    # dmp['vav_cfm'].hasExternalReference = TimeSeriesReference
    # dmp['vav_eat'].hasExternalReference = TimeSeriesReference

    dmp["vav_dp"].hasMeasurementLocation = dmp.airInlet
    dmp["vav_cfm"].hasMeasurementLocation = dmp.airInlet
    dmp["vav_eat"].hasMeasurementLocation = dmp.airInlet
    return dmp


def ext_ref_fan(label, ext_ref=None):
    f = Fan(config=fan_template, label=label)
    vfd = VFD(config=vfd_template)
    hsf_wat = ElectricPowerW
    hsf_spd = PercentAngularVelocity
    vfd.W = hsf_wat
    hsf_wat.hasExternalReference = TimeSeriesReference
    vfd.spd = hsf_spd
    hsf_spd.hasExternalReference = TimeSeriesReference

    f > vfd  # include VFD in Fan
    vfd >> f  # connect electricity
    return f


# this feels wrong, but not sure what else would be right
class VAV_Mixing_Box(Equipment):
    hotAirInlet: AirInletConnectionPoint
    coldAirInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


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
        hsf = ext_ref_fan(label=self.label + ".hot_supply_fan")
        self.airOutlet.mapsTo = hsf.airOutlet
        in_filter >> hwc >> hsf

        # ext_ref1= TimeSeriesReference()
        # hsf.sensors['TPD1'].hasExternalReference = ext_ref1
        hsf_dp = AirDifferentialPressureSensor(label=self.label + ".fan_dp_sensor")
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
    temp_sp: TemperatureSetpoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        in_filter = Filter(label=self.label + ".filter")
        self.airInlet.mapsTo = in_filter.airInlet
        hwc = HotWaterCoil2(label=self.label + ".cold_water_coil")
        hsf = ext_ref_fan(label=self.label + ".hot_supply_fan")
        self.airOutlet.mapsTo = hsf.airOutlet
        in_filter >> hwc >> hsf

        # ext_ref1= TimeSeriesReference()
        # hsf.sensors['TPD1'].hasExternalReference = ext_ref1
        hsf_dp = AirDifferentialPressureSensor(label=self.label + ".fan_dp_sensor")
        hsf_dp.hasMeasurementLocationHigh = hsf.airOutlet
        hsf_dp.hasMeasurementLocationLow = hsf.airInlet

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

        return_air_fan = Fan(label=self.label + ".return_air_fan", config=fan_template)
        self.returnAirInlet.mapsTo = return_air_fan.airInlet

        re_dat = AirTemperatureSensor(label=self.label + ".re_air_temp_sensor")
        re_humd = AirHumiditySensor(label=self.label + ".re_air_humidity_sensor")
        re_cfm = AirFlowSensor(label=self.label + ".re_air_flow_sensor")

        re_dat.hasMeasurementLocation = return_air_fan.airInlet
        re_humd.hasMeasurementLocation = return_air_fan.airInlet
        re_cfm.hasMeasurementLocation = return_air_fan.airInlet
        # sensors here and about fan

        # j1 = Junction()
        # j1.link_to(return_air_fan.airOutlet)

        recirc_damper = Damper(label=self.label + ".recirculated_air_damper")
        exhaust_damper = Damper(label=self.label + ".exhaust_damper")

        # j1.link_to(recirc_damper.airInlet)
        # j1.link_to(exhaust_damper.airInlet)
        return_air_fan >> [recirc_damper, exhaust_damper]

        self.exhaustAirOutlet.mapsTo = exhaust_damper.airOutlet

        recirc_damper >> mixed_air

        hot_deck = HotDeck(label=self.label + ".hot_deck")
        mixed_air >> hot_deck.airInlet

        cold_deck = ColdDeck(label=self.label + ".cold_deck")
        mixed_air >> cold_deck

        self.supplyColdAirOutlet.mapsTo = cold_deck.airOutlet
        self.supplyHotAirOutlet.mapsTo = hot_deck.airOutlet


class ddahu_VAV(System):
    hotAirInlet: AirInletSystemConnectionPoint
    coldAirInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    node_type = p223.TerminalUnit

    def __init__(self, ext_ref_dict=None, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        hot_dmp = ext_ref_damper(label=self.label + ".hot_damper")
        cold_dmp = ext_ref_damper(label=self.label + ".cold_damper")
        self.hotAirInlet.mapsTo = hot_dmp.airInlet
        self.coldAirInlet.mapsTo = cold_dmp.airInlet

        mb = VAV_Mixing_Box(
            label=self.label + ".mixing_box", config=mixing_box_template
        )
        mb["vav_eat"].hasMeasurementLocation = mb.airOutlet

        hot_dmp >> mb.hotAirInlet
        cold_dmp >> mb.coldAirInlet

        self.airOutlet.mapsTo = mb.airOutlet


class HVAC_rooms(DomainSpace):
    hasDomain = HVAC
    hasMedium: Medium = Air

    def __init__(self, ext_ref_dict=None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        rm_temp = AirTemperatureSensor(label="rm_temp")
        rm_temp.hasMeasurementLocation = self
        rm_temp.hasExternalReference = TimeSeriesReference()


# could easily run this from a generic spreadsheet/csv
def DDAHU_assembler():
    ddahu_refs = ext_ref.get("ddahu_refs")
    ddahu = DDAHU(label="DDAHU", ext_ref_dict=ddahu_refs)


# ddvav = ddahu_VAV(label = 'test vav')
h = HVAC_rooms(label="ate")
# ddahu = DDAHU(label="DDAHU")
# vfd = VFD(label = 'vfd', properties = {'Electric_Power': Electric_Power})
# vfd.properties['Electric_Power'].hasSetpoint = ep
lbnl_header(model_name)
dump()
