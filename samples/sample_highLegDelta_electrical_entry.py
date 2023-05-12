from pathlib import Path
from typing import Any
from bob.enum import CtxAttribute, ElectricalPhaseIdentifier
from bob.equipment.electricity.meter import ThreePhaseElectricalMeter
from bob.connections.electricity import (
    Electricity_240V_208V_120V_3Ph_60HzOutletConnectionPoint,
    Electricity_240V_208V_120V_3Ph_60HzConnection,
)

from header import sample_header

from bob.connections.air import *
from bob.connections.electricity import *
from bob.connections.light import LightVisibleConnection
from bob.connections.occupancy import (
    OccupancyInletSystemConnectionPoint,
    OccupancyOutletSystemConnectionPoint,
)
from bob.core import P223, QUANTITYKIND, UNIT, bind_model_namespace, dump, get_datagraph
from bob.equipment.architectural import Window
from bob.equipment.electricity.distribution import (
    SinglePhaseDistributionPanel,
    SinglePoleCircuitBreaker,
    ThreePhaseDistributionPanel,
    ThreePolesCircuitBreaker,
    ThreePolesMainCircuitBreaker,
    Transformer,
    TwoPolesCircuitBreaker,
    TwoPolesMainCircuitBreaker,
)
from bob.equipment.hvac.airhandlingunit import AirHandlingUnit
from bob.equipment.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.equipment.hvac.damper import ElectricalActuatedProportionalDamper
from bob.equipment.hvac.fan import Fan
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.vav import VAV
from bob.equipment.lighting.light import Luminaire
from bob.property import QuantifiableObservableProperty
from bob.sensor.flow import AirFlowSensor
from bob.sensor.temperature import AirTemperatureSensor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace, LightingZone
from bob.space.physical import Bathroom, Building, Corridor, Floor, Office, Roof, Room

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# Define breaker in template
mainentry_panel_config = {
    "params": {
        "label": "Main Entry Panel",
        "comment": "Main Entry Panel of Building using High Leg Delta Configuration",
        "voltage": "HighLeg",
    },
    "sensors": {},
    "equipment": {
        ("MainBreaker", ThreePolesMainCircuitBreaker): {
            "comment": "Main breaker of panel",
            "amps": 400,
            "voltage": "HighLeg",
        },
        ("CB#1", SinglePoleCircuitBreaker): {
            "comment": "120V 1 Hot Neutral",
            "amps": 15,
            "voltage": "120",
            "bus_bar": "A",
        },
        ("CB#2", ThreePolesCircuitBreaker): {
            "comment": "240V 3 phases",
            "amps": 40,
            "voltage": "240",
        },
        ("CB#3", TwoPolesCircuitBreaker): {
            "comment": "2 Hot",
            "amps": 100,
            "voltage": "240",
            "bus_bar": "AB",
        },
        ("CB#4", SinglePoleCircuitBreaker): {
            "comment": "High Leg Neutral",
            "amps": 15,
            "bus_bar": "C",
            "voltage": "208",
        },
    },
    # other properties could go there... ?
}


def test_electrical_entry():
    # Electrical Equipment

    main_panel = ThreePhaseDistributionPanel(config=mainentry_panel_config)

    transformer_120_208_240_connection = (
        Electricity_240V_208V_120V_3Ph_60HzConnection(label="HighLegDeltaTransfoOutput")
        + ElectricalPhaseIdentifier.ABC
    )

    transformer_120_208_240_connection >> main_panel["MainBreaker"]

    return main_panel


if __name__ == "__main__":
    r = test_electrical_entry()
    dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
