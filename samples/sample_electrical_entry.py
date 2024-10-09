from pathlib import Path

from bob.scratch.header import sample_header

from bob.connections.air import *
from bob.connections.electricity import (
    Electricity_240VLL_120VLN_1Ph_60HzOutletConnectionPoint,
    Electricity_600VLL_3Ph_60HzConnection,
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
)
from bob.core import (
    bind_model_namespace,
    dump,
)
from bob.enum import Electricity, ElectricalPhaseIdentifier
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
from bob.equipment.electricity.meter import ThreePhaseElectricalMeter

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


# Define breaker in template
mainentry_panel_config = {
    "params": {
        "label": "Main Entry Panel",
        "comment": "Main Entry Panel of Building at 600V_3Ph",
        "voltage": "575",
    },
    "sensors": {},
    "equipment": {
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
        ("CB#4", ThreePolesCircuitBreaker): {
            "comment": "Used for Meter",
            "amps": 15,
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
    "equipment": {
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
    # Electrical Equipment

    main_panel = ThreePhaseDistributionPanel(config=mainentry_panel_config)
    transformer_120_240 = Transformer(
        label="TX-1",
        electricalInlet=Electricity_600VLL_3Ph_60HzInletConnectionPoint,
        electricalOutlet=Electricity_240VLL_120VLN_1Ph_60HzOutletConnectionPoint,
    )

    dist_panel = SinglePhaseDistributionPanel(config=distribution_panel_config)
    # hq = Electricity_240VLL_120VLN_1Ph_60HzConnection(label='Hydro-Québec', comment="That would be for a home...")
    hq_600 = Electricity_600VLL_3Ph_60HzConnection(label="Hydro-Québec", comment="600V")
    hq_600 += ElectricalPhaseIdentifier.ABC
    hq_600 >> main_panel["MainBreaker"]
    main_panel["CB#3"] >> transformer_120_240 >> dist_panel["MainBreaker"]

    building_electrical_meter = ThreePhaseElectricalMeter(
        label="Building Meter",
        comment="Building Electrical Meter (M3)",
        medium=Electricity.AC600VLL_3Ph_60Hz,
    )
    # building_electrical_meter.hasPhysicalLocation = ps.bldg
    building_electrical_meter.set_voltage_measurement_location(main_panel["CB#4"])
    building_electrical_meter.set_current_measurement_location(
        main_panel["MainBreaker"].electricalInlet
    )
    return main_panel


if __name__ == "__main__":
    r = test_electrical_entry()
    dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
