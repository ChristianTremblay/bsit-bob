from copy import copy

from bob.core import (
    bind_model_namespace,
    dump,
    quantitykind,
    unit,
)

from bob.devices.hvac.gas import GasMonitor
from bob.property import QuantifiableObservableProperty
from bob.sensor.gas import CO2Sensor, NO2Sensor, COSensor
from bob.sensor.temperature import AirTemperatureSensor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.physical import Building, Roof, Floor, Office

from pathlib import Path
from header import ttl_test_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


def test_create_gaz_monitor():
    _config_co2_and_temp = {
        "params": {
            "label": "CO2-2",
            "comment": "CO2 Monitor with temperature reading",
        },
        "sensors": {
            ("CO2_sensor", CO2Sensor): {
                "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO2_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    2000,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO2_sensor.MaxRange",
                ),
            },
            ("Temperature_sensor", AirTemperatureSensor): {
                # "measuresSubstance": enum["Medium-Air"],
                "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=quantitykind.Temperature,
                    unit=unit.DEG_C,
                    label="Temperature_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    50,
                    hasQuantityKind=quantitykind.Temperature,
                    unit=unit.DEG_C,
                    label="Temperature_sensor.MaxRange",
                ),
                "comment": "Internal temperature sensor of device",
            },
        },
    }

    dual_no2_co_configuration_example = {
        "sensors": {
            ("CO_sensor", COSensor): {
                "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    100,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO_sensor.MaxRange",
                ),
            },
            ("NO2_sensor", NO2Sensor): {
                "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="NO2_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    250,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="NO2_sensor.MaxRange",
                ),
            },
        }
    }

    dualgasmonitor = GasMonitor(
        label="GM-1",
        comment="Dual Gas Monitoring Device that measure NO2 and CO. Usually used in underground parking lot",
        config=dual_no2_co_configuration_example,
    )

    co2monitor_config = {
        "sensors": {
            ("CO2_sensor", CO2Sensor): {
                "hasExternalReference": "bacnet://",
                "hasMinRange": QuantifiableObservableProperty(
                    0,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO2_sensor.MinRange",
                ),
                "hasMaxRange": QuantifiableObservableProperty(
                    2000,
                    hasQuantityKind=quantitykind.DimensionlessRatio,
                    unit=unit.PPM,
                    label="CO2_sensor.MaxRange",
                ),
            },
        }
    }

    co2monitor = GasMonitor(
        label="CO2-1",
        comment="CO2 Monitor",
        config=co2monitor_config,
    )

    co2monitor = GasMonitor(
        config=_config_co2_and_temp,
    )

    _config = copy(_config_co2_and_temp)
    _config["params"]["label"] = "CO2-4"
    co2monitor = GasMonitor(
        label="CO2-4",
        comment="CO2 Monitor in basement",
        config=_config,
    )

    building = Building(label="My Building")
    roof = Roof(label="Roof of building")
    floor = Floor(label="Floor1")
    basement = Floor(label="Basement")
    office1 = Office(label="Office 1")
    office2 = Office(label="Office 2")
    office3 = Office(label="Office 3")
    joelsoffice = Office(label="Joel's Office")

    office1_hvac = HVACSpace(label="Office 1")
    office2_hvac = HVACSpace(label="Office 2")
    office3_hvac = HVACSpace(label="Office 3")
    basementhvac = HVACSpace(label="Basement HVAC Space")

    zone1 = HVACZone(label="Zone1")

    # Physical relationships
    building > roof
    building > floor
    building > basement > basementhvac
    basement > joelsoffice
    floor > office1
    floor > office2
    floor > office3

    # Spaces relationships
    # SPACES     | PHYSICAL
    office1_hvac < office1
    office2_hvac < office2
    office3_hvac < office3

    # basementhvac < basement

    # Zones (group of spaces)
    # Here, Zone1 contains office1 and office2
    office1_hvac < zone1
    office2_hvac < zone1

    co2monitor.hasPhysicalLocation = basement
    co2monitor["CO2_sensor"].hasMeasurementLocation = basementhvac
    co2monitor["Temperature_sensor"].hasMeasurementLocation = basementhvac

    dump(filename=f"tests/ttl/{model_name}.ttl", header=ttl_test_header(model_name))
