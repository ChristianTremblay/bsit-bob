"""
Dual Duct AHU

creating christian style
REVISIT COILS
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
    Air,
    Device,
    DomainSpace,
    Junction,
    System,
    bind_model_namespace,
    dump,
    p223,
    quantitykind,
    unit,
)
from bob.equipments.archives.coolingcoil import ChilledWaterCoil2
from bob.equipments.archives.heatingcoil import HotWaterCoil2

# from bob.equipments.hvac.airhandlingunit import AirHandlingUnit
from bob.equipments.hvac.damper import Damper
from bob.equipments.hvac.fan import Fan
from bob.equipments.hvac.filter import Filter
from bob.equipments.hvac.vfd import VFD
from bob.externalreference.timeseries import TimeSeriesReference
from bob.properties.electricity import ElectricPower, ElectricPowerkW, ElectricPowerW
from bob.properties.ratio import Percent, PercentAngularVelocity
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

# Maybe fan should contain VFD. I think it would simplify querying in some cases.


class DDAHU(System):
    outsideAirInlet: AirInletSystemConnectionPoint
    returnAirInlet: AirInletSystemConnectionPoint
    supplyHotAirOutlet: AirOutletSystemConnectionPoint
    supplyColdAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)

    def assemble(self):
        # ddahu = DDAHU(config = ddahu_template, label = 'ddahu')
        self["oa_dat"].hasMeasurementLocation = self["oa_damper"].airInlet
        self["oa_humd"].hasMeasurementLocation = self["oa_damper"].airInlet
        self["oa_cfm"].hasMeasurementLocation = self["oa_damper"].airInlet

        self.outsideAirInlet.mapsTo = self["oa_damper"].airInlet

        mixed_air = AirConnection(label=self.label + ".mixed_air")
        self["oa_damper"] >> mixed_air
        self["ma_temp"].hasMeasurementLocation = mixed_air

        self.returnAirInlet.mapsTo = self["return_air_fan"].airInlet

        self["re_dat"].hasMeasurementLocation = self["return_air_fan"].airInlet
        self["re_humd"].hasMeasurementLocation = self["return_air_fan"].airInlet
        self["re_cfm"].hasMeasurementLocation = self["return_air_fan"].airInlet

        self["return_air_fan"] >> [self["recirc_damper"], self["exhaust_damper"]]

        self.exhaustAirOutlet.mapsTo = self["exhaust_damper"].airOutlet

        self["recirc_damper"] >> mixed_air
        mixed_air >> self["hot_deck"]
        mixed_air >> self["cold_deck"]

        self.supplyColdAirOutlet.mapsTo = self["cold_deck"].airOutlet
        self.supplyHotAirOutlet.mapsTo = self["hot_deck"].airOutlet


class ddahu_fan(Fan):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def assemble(self):
        self["vfd"] >> self
        self["TPD1"].hasMeasurementLocationHigh = self.airOutlet
        self["TPD1"].hasMeasurementLocationLow = self.airInlet


# in_filter, coil, supply_fan,  airdiff pressure on fan?
class HotColdDeck(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    temp_sp: PropertyReference

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def assemble(self):
        self.airInlet.mapsTo = self["in_filter"].airInlet
        self.airOutlet.mapsTo = self["supply_fan"].airOutlet
        self["in_filter"] >> self["coil"] >> self["supply_fan"]
        self["temp"].observesProperty.hasSetpoint = self.temp_sp
        self["dat"].hasMeasurementLocation = self["coil"].airOutlet
        self["humd"].hasMeasurementLocation = self["supply_fan"].airOutlet
        self["cfm"].hasMeasurementLocation = self["supply_fan"].airOutlet
        self["temp"].hasMeasurementLocation = self["supply_fan"].airOutlet


# this feels wrong, but not sure what else would be right
class VAV_Mixing_Box(Device):
    hotAirInlet: AirInletConnectionPoint
    coldAirInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    #    temp_sp: TemperatureSetpoint
    temp_sp: PropertyReference

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class ddahu_VAV(System):
    hotAirInlet: AirInletSystemConnectionPoint
    coldAirInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    node_type = p223.TerminalUnit

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def assemble(self):
        self["hot_dmp"]["vav_dp"].hasMeasurementLocation = self["hot_dmp"].airInlet
        self["hot_dmp"]["vav_cfm"].hasMeasurementLocation = self["hot_dmp"].airInlet
        self["hot_dmp"]["vav_eat"].hasMeasurementLocation = self["hot_dmp"].airInlet

        self["cold_dmp"]["vav_dp"].hasMeasurementLocation = self["cold_dmp"].airInlet
        self["cold_dmp"]["vav_cfm"].hasMeasurementLocation = self["cold_dmp"].airInlet
        self["cold_dmp"]["vav_eat"].hasMeasurementLocation = self["cold_dmp"].airInlet

        self.hotAirInlet.mapsTo = self["hot_dmp"].airInlet
        self.coldAirInlet.mapsTo = self["cold_dmp"].airInlet

        self["vav_eat"].hasMeasurementLocation = self["mb"].airOutlet

        self["hot_dmp"] >> self["mb"].hotAirInlet
        self["cold_dmp"] >> self["mb"].coldAirInlet

        self.airOutlet.mapsTo = self["mb"].airOutlet


class HVAC_rooms(DomainSpace):
    hasDomain = HVAC
    hasMedium: Medium = Air

    def __init__(self, ext_ref_dict=None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        rm_temp = AirTemperatureSensor(label="rm_temp")
        rm_temp.hasMeasurementLocation = self
        rm_temp.hasExternalReference = TimeSeriesReference()


# add properties to config?
# Devices DON'T have properties as default, but have a default config that you can optionally use.

# should separate units from electric power.
vfd_template = {
    "params": {
        "label": "MyVFD",
        "comment": "A VFD for a Big Fan",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
        "W": ElectricPowerW(hasExternalReference=TimeSeriesReference()),
        "speed_reference": Percent(hasExternalReference=TimeSeriesReference()),
    },
    "sensors": {},
    "devices": {},
}
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
    "devices": {("vfd", VFD): {"config": vfd_template}},
}

hot_deck_template = {
    "params": {"label": "hot deck"},
    "sensors": {
        ("dat", AirTemperatureSensor): {},
        ("humd", AirHumiditySensor): {},
        ("cfm", AirFlowSensor): {},
        ("temp", AirTemperatureSensor): {},
    },
    "devices": {
        ("coil", HotWaterCoil2): {},
        ("in_filter", Filter): {},
        ("supply_fan", ddahu_fan): {"config": fan_template},
    },
}

cold_deck_template = {
    "params": {"label": "cold deck"},
    "sensors": {
        ("dat", AirTemperatureSensor): {},
        ("humd", AirHumiditySensor): {},
        ("cfm", AirFlowSensor): {},
        ("temp", AirTemperatureSensor): {},
    },
    "devices": {
        ("coil", ChilledWaterCoil2): {},
        ("in_filter", Filter): {},
        ("supply_fan", ddahu_fan): {},
    },
}

vav_damper_template = {
    "params": {"label": "vav damper", "comment": "A hot or cold damper"},
    "sensors": {
        ("vav_eat", AirTemperatureSensor): {
            "comment": "Air Temperature Sensor",
            "hasExternalReference": TimeSeriesReference,
        },
        ("vav_cfm", AirFlowSensor): {},
        ("vav_dp", AirStaticPressureSensor): {},
    },
    "devices": {},
}

vav_template = {
    "params": {"label": "vav", "comment": "vav for dual duct system"},
    "sensors": {
        ("vav_eat", AirTemperatureSensor): {
            "comment": "Air Temperature Sensor",
            "hasExternalReference": TimeSeriesReference,
        },
    },
    "devices": {
        ("hot_dmp", Damper): {"config": vav_damper_template},
        ("cold_dmp", Damper): {"config": vav_damper_template},
        ("mb", VAV_Mixing_Box): {},
    },
}
# d = ddahu_VAV(config = vav_template, label = 'vav')
# d.assemble()

ddahu_template = {
    "params": {"label": "ddahu", "comment": "ddahu"},
    "sensors": {
        ("oa_dat", AirTemperatureSensor): {},
        ("oa_humd", AirHumiditySensor): {},
        ("oa_cfm", AirFlowSensor): {},
        ("ma_temp", AirTemperatureSensor): {},
        ("re_dat", AirTemperatureSensor): {},
        ("re_humd", AirHumiditySensor): {},
        ("re_cfm", AirFlowSensor): {},
    },
    "devices": {
        ("oa_damper", Damper): {"comment": ".oa_damper"},
        ("recirc_damper", Damper): {"comment": ".recirc_damper"},
        ("exhaust_damper", Damper): {"comment": ".ea_damper"},
        ("return_air_fan", Fan): {"comment": "return_fan"},
    },
    "systems": {
        ("hot_deck", HotColdDeck): {
            "comment": ".hot_deck",
            "config": hot_deck_template,
        },
        ("cold_deck", HotColdDeck): {
            "comment": ".cold_deck",
            "config": cold_deck_template,
        },
    },
}

"""
csv like for brick building
create ddahu
use .loc to get hot and cold decks, 
one row for labels, point names, and UUID's
use .loc and get to get uuid's and fill in templates
create each thing manually. 
json/dict style config would be better, but this will do. 
"""
d = ddahu_fan(label="f", config=fan_template)
d.assemble()
# ddahu = DDAHU(label="DDAHU", config = ddahu_template)
# ddahu.assemble()
# mb = VAV_Mixing_Box(label = 'mb', config = mixing_box_template, temp_sp = TemperatureSetpoint(hasExternalReference = TimeSeriesReference('abc')))
# vfd = VFD(label = 'vfd', properties = {'Electric_Power': Electric_Power})
# vfd.properties['Electric_Power'].hasSetpoint = ep
lbnl_header(model_name)
dump()
