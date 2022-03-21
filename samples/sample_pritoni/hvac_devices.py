from bob.devices.hvac.coil import HotWaterCoil
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.damper import ElectricalActuatedDamper, Window
from bob.sensor.flow import AirFlowSensor
from bob.sensor.temperature import AirTemperatureSensor
from bob.systems.hvac.vav import VAV

import hvac_spaces as hs

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
