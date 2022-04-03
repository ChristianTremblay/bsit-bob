from cProfile import label
from pathlib import Path

from typing import Any

from bob.connections.light import LightVisibleConnection
from bob.connections.occupancy import (
    OccupancyInletSystemConnectionPoint,
    OccupancyOutletSystemConnectionPoint,
)

from bob.core import p223, get_datagraph, bind_model_namespace, dump, quantitykind, unit

from bob.devices.hvac.damper import ElectricalActuatedDamper
from bob.devices.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.damper import Window
from bob.devices.lighting.light import Luminaire

from bob.devices.electricity.distribution import (
    Transformer,
    SinglePhaseDistributionPanel,
    SinglePoleCircuitBreaker,
    ThreePhaseDistributionPanel,
    ThreePolesCircuitBreaker,
    ThreePolesMainCircuitBreaker,
    TwoPolesCircuitBreaker,
    TwoPolesMainCircuitBreaker,
)
from bob.property import QuantifiableObservableProperty

from bob.space.occupancy import OccupancySpace
from bob.systems.hvac.airhandlingunit import AirHandlingUnit
from bob.systems.hvac.vav import VAV
from bob.sensor.temperature import AirTemperatureSensor
from bob.sensor.flow import AirFlowSensor
from bob.sensor.movement import MovementSensor, OccupancySensor

from bob.space.physical import Building, Floor, Roof, Office, Room, Bathroom, Corridor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace, LightingZone

from bob.systems.functionblock import FunctionBlock

from bob.connections.air import *
from bob.connections.electricity import *

from header import sample_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# Define breaker in template
mainentry_panel_config = {
    "params": {
        "label": "Main Entry Panel",
        "comment": "Main Entry Panel of Building at 575V",
        "voltage": "575",
    },
    "sensors": {},
    "devices": {
        ("MainBreaker", ThreePolesMainCircuitBreaker): {
            "comment": "Main breaker of panel",
            "amps": 400,
            "voltage": "575",
        },
        ("CB#1", SinglePoleCircuitBreaker): {
            "comment": "Lights",
            "amps": 15,
            "voltage": 347,
            "bus_bar": "A",
        },
        ("CB#2", ThreePolesCircuitBreaker): {
            "comment": "Fans, AHU",
            "amps": 40,
            "voltage": "575",
        },
        ("CB#3", ThreePolesCircuitBreaker): {
            "comment": "Feeds Transformer to get 120/240",
            "amps": 100,
            "voltage": "575",
        },
    },
    # other properties could go there... ?
}

distribution_panel_config = {
    "params": {
        "label": "My Panel",
        "comment": "Description of my panel",
        "voltage": "120_240",
    },
    "sensors": {},
    "devices": {
        ("MainBreaker", TwoPolesMainCircuitBreaker): {
            "comment": "Main breaker of panel",
            "amps": 200,
            "voltage": "120_240",
        },
        ("CB#1", SinglePoleCircuitBreaker): {
            "comment": "Lights",
            "amps": 15,
            "voltage": "120",
            "bus_bar": "A",
        },
        ("CB#2", TwoPolesCircuitBreaker): {
            "comment": "Heater",
            "amps": 20,
            "voltage": "240",
        },
    },
    # other properties could go there... ?
}


def test_electrical_entry():
    # Electrical devices

    main_panel = ThreePhaseDistributionPanel(config=mainentry_panel_config)
    transformer_120_240 = Transformer(
        label="TX-1",
        electricalInlet=Electricity_575V_60HzInletConnectionPoint,
        electricalOutlet=Electricity_120V_240V_60HzOutletConnectionPoint,
    )

    dist_panel = SinglePhaseDistributionPanel(config=distribution_panel_config)
    # hq = Electricity_120V_240V_60HzConnection(label='Hydro-Québec', comment="That would be for a home...")
    hq_600 = Electricity_575V_60HzConnection(label="Hydro-Québec", comment="600V")
    hq_600 >> main_panel["MainBreaker"]
    main_panel["CB#3"] >> transformer_120_240 >> dist_panel["MainBreaker"]


if __name__ == "__main__":
    r = test_electrical_entry()
    dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
