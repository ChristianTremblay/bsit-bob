from pathlib import Path

from bob.connections.electricity import *
from bob.core import bind_model_namespace, dump
from bob.devices.electricity.distribution import *

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


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
            "comment": "Parking Lot Lights",
            "amps": 15,
            "voltage": 347,
            "bus_bar": "A",
        },
        ("CB#2", ThreePolesCircuitBreaker): {
            "comment": "Supply Fans, AHU",
            "amps": 40,
            "voltage": "575",
        },
        ("CB#3", ThreePolesCircuitBreaker): {
            "comment": "Feeds Transformer to get 120/240",
            "amps": 100,
            "voltage": "575",
        },
        ("CB#4", ThreePolesCircuitBreaker): {
            "comment": "Return Fans, AHU",
            "amps": 40,
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
            "comment": "Lights in OpenOffice",
            "amps": 15,
            "voltage": "120",
            "bus_bar": "A",
        },
        ("CB#2", TwoPolesCircuitBreaker): {
            "comment": "Heater",
            "amps": 20,
            "voltage": "240",
        },
        ("CB#3", SinglePoleCircuitBreaker): {
            "comment": "Lights in Kitchenette",
            "amps": 15,
            "voltage": "120",
            "bus_bar": "A",
        },
        ("CB#4", SinglePoleCircuitBreaker): {
            "comment": "Lights in Corridors + bathroom",
            "amps": 15,
            "voltage": "120",
            "bus_bar": "A",
        },
        ("CB#5", SinglePoleCircuitBreaker): {
            "comment": "Lights in Private Office",
            "amps": 15,
            "voltage": "120",
            "bus_bar": "A",
        },
    },
    # other properties could go there... ?
}
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


# We need a trough so light breakers will be connected to multiple loads
dist_panel_cb1 = Electricity_120V_60HzConnection(label="DISTPANEL-CB1")
dist_panel_cb3 = Electricity_120V_60HzConnection(label="DISTPANEL-CB3")
dist_panel_cb4 = Electricity_120V_60HzConnection(label="DISTPANEL-CB4")
dist_panel_cb5 = Electricity_120V_60HzConnection(label="DISTPANEL-CB5")
dist_panel["CB#1"] >> dist_panel_cb1
dist_panel["CB#3"] >> dist_panel_cb3
dist_panel["CB#4"] >> dist_panel_cb4
dist_panel["CB#5"] >> dist_panel_cb5

if __name__ == "__main__":
    dump()
