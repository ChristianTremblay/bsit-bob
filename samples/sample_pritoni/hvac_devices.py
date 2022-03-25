from bob.connections.electricity import (
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
)
from bob.devices.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.damper import ElectricalActuatedDamper, Window
from bob.devices.hvac.vfd import VFD
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.stats import DifferentialStaticPressureSensor
from bob.devices.electricity.starter import MotorStarter
from bob.sensor.flow import AirFlowSensor
from bob.sensor.pressure import DifferentialStaticPressure
from bob.sensor.temperature import AirTemperatureSensor
from bob.systems.hvac.airhandlingunit import AirHandlingUnit
from bob.systems.hvac.vav import VAV


import hvac_spaces as hs

ahu_template = {
    "params": {"label": "AHU", "comment": "AHU delivering air to 2 VAV boxes"},
    "sensors": {
        ("OA-T", AirTemperatureSensor): {"comment": "Oudoor air temperature"},
        ("TPD1", DifferentialStaticPressureSensor): {
            "comment": "Filter Differential Pressure Sensor"
        },
        ("HC-T", AirTemperatureSensor): {
            "comment": "Air temperature after heating coil"
        },
        ("DA-T", AirTemperatureSensor): {
            "comment": "Discharge Air temperature after cooling coil"
        },
        ("TPD2", DifferentialStaticPressure): {
            "comment": "Supply Duct Static Pressure"
        },
        ("TPD3", DifferentialStaticPressure): {
            "comment": "Return Duct Static Pressure"
        },
    },
    "contains": {
        ("RF", Fan): {
            "comment": "Return Air Fan",
            "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        },
        ("SF", Fan): {
            "comment": "Supply Air Fan",
            "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        },
        ("SF-STARTER", MotorStarter): {
            "comment": "Supply Air Fan Starter",
            "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
            "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
        },
        ("RF-VFD", VFD): {
            "comment": "VFD for return Fan",
            "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
            "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
        },
        ("CLGCOIL", ChilledWaterCoil): {"comment": "Cooling Coil"},
        ("HTGCOIL", HotWaterCoil): {"comment": "Heating coil"},
        ("FILTER", Filter): {"comment": "Filter"},
        ("OADPR", ElectricalActuatedDamper): {"comment": "Outdoor air damper"},
        ("MADPR", ElectricalActuatedDamper): {"comment": "Mixed Air Damper"},
        ("EADPR", ElectricalActuatedDamper): {"comment": "Exhaust Air Damper"},
    },
}

vav1_config = {
    "params": {"label": "VAVBox1", "comment": "VAV Serving HVAC Zone 1"},
    "sensors": {
        ("VAV1_SA-F", AirFlowSensor): {"comment": "Air flow used to control damper"},
        ("VAV1_DA-T", AirTemperatureSensor): {
            "comment": "Air supplied to zone by VAV 1, AKA discharge air temperature"
        },
        ("VAV1_ZN-T", AirTemperatureSensor): {
            "comment": "Zone Air Temperature Sensor, which is a thermostats..."
        },
    },
    "contains": {
        ("VAV1_damper", ElectricalActuatedDamper): {"comment": "VAV Box 1 Air Damper"},
        ("VAV1_HeatingCoil", HotWaterCoil): {"comment": "VAV Box 1 Hot Water Coil"},
    },
}

vav2_config = {
    "params": {"label": "VAVBox2", "comment": "VAV Serving HVAC Zone 2"},
    "sensors": {
        ("VAV2_SA-F", AirFlowSensor): {"comment": "Air flow used to control damper"},
        ("VAV2_DA-T", AirTemperatureSensor): {
            "comment": "Air supplied to zone by VAV 2, AKA discharge air temperature"
        },
        ("VAV2_ZN-T", AirTemperatureSensor): {
            "comment": "Zone Air Temperature Sensor, which is a thermostats..."
        },
    },
    "contains": {
        ("VAV2_damper", ElectricalActuatedDamper): {"comment": "VAV Box 2 Air Damper"},
        ("VAV2_HeatingCoil", HotWaterCoil): {"comment": "VAV Box 2 Hot Water Coil"},
    },
}

ahu = AirHandlingUnit(config=ahu_template)


bathroom_exhaust_fan = Fan(label="ExhaustFan", comment="Bathroom exhaust fan")
window1 = Window(
    label="Window_West",
    comment="First Window in OpenOffice, covering West portion of room",
)
window2 = Window(
    label="Window_East",
    comment="Second Window in OpenOffice, covering East portion of room",
)

vav1 = VAV(config=vav1_config)
vav1.servesZone = hs.hvac_zone_1
vav2 = VAV(config=vav2_config)
vav2.servesZone = hs.hvac_zone_2
