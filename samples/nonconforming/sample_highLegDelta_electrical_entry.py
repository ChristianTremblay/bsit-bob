from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.connections.air import *
from bob.connections.electricity import *
from bob.connections.electricity import (
    Electricity_240VLL_208VLN_120VLN_3Ph_60HzConnection,
)
from bob.core import bind_model_namespace, dump
from bob.enum import ElectricalPhaseIdentifier
from bob.equipment.electricity.distribution import (
    SinglePoleCircuitBreaker,
    ThreePhaseDistributionPanel,
    ThreePolesCircuitBreaker,
    ThreePolesMainCircuitBreaker,
    TwoPolesCircuitBreaker,
)
from bob.scratch.header import sample_header

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
        ("CB#5", SinglePoleCircuitBreaker): {
            "comment": "High Leg Neutral, second breaker",
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
        Electricity_240VLL_208VLN_120VLN_3Ph_60HzConnection(
            label="HighLegDeltaTransfoOutput"
        )
    )
    transformer_120_208_240_connection += ElectricalPhaseIdentifier.ABC

    transformer_120_208_240_connection >> main_panel["MainBreaker"]

    return main_panel


if __name__ == "__main__":
    r = test_electrical_entry()
    _folder = Path(__file__).parent
    create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
