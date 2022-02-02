from bob.core import (
    bind_model_namespace,
    dump,
    turtle,
    ExternalReference,
    get_datagraph,
    Value,
    quantitykind,
    unit,
    enum,
)

from bob.devices.electricity.distribution_wip import DistributionPanel, CircuitBreaker
from bob.connections.electricity import (
    Electricity_120V_60HzInletConnectionPoint,
    Electricity_120V_60HzOutletConnectionPoint,
    Electricity_240V_60HzInletConnectionPoint,
    Electricity_240V_60HzOutletConnectionPoint,
    Electricity_120V_240V_60HzInletConnectionPoint,
)

__namespace__ = bind_model_namespace("ex", "urn:ex/")


def test_create_emptyelectricalpaneldevice():
    distributionpanel_template = {
        "params": {
            "label": "Name Of Panel",
            "comment": "Description",
            "electricalInlet": Electricity_120V_240V_60HzInletConnectionPoint,
            "electricalOutletA": Electricity_120V_60HzOutletConnectionPoint,
            "electricalOutletB": Electricity_240V_60HzOutletConnectionPoint,
            # "hasMeasurementLocation": Connection,
        },
        "sensors": {},
        "contains": {},
        # other properties could go there... ?
    }
    elc_panel = DistributionPanel(
        label="P-1",
        comment="Electrical panel full of breakers. 120V-240VAC 60Hz",
        config=distributionpanel_template,
    )

    return elc_panel


def test_create_electricalpaneldevice():
    distributionpanel_template = {
        "params": {
            "label": "Name Of Panel",
            "comment": "Description",
            "electricalInlet": Electricity_120V_240V_60HzInletConnectionPoint,
            "electricalOutletA": Electricity_120V_60HzOutletConnectionPoint,
            "electricalOutletB": Electricity_240V_60HzOutletConnectionPoint,
            # "hasMeasurementLocation": Connection,
        },
        "sensors": {},
        "contains": {
            ("CircBreaker_120_#1", CircuitBreaker): {
                "comment": "Office lights #1",
                "hasSubstance": enum["Electricity-120V.60Hz"],
                "electricalInlet": Electricity_120V_60HzInletConnectionPoint,
                "electricalOutlet": Electricity_120V_60HzOutletConnectionPoint,
                "hasMaxRange": Value(
                    15, hasQuantityKind=quantitykind.ElectricCurrent, unit=unit.A
                ),
            },
            ("CircBreaker_240_#2", CircuitBreaker): {
                "comment": "Heating Room #1",
                "hasSubstance": enum["Electricity-240V.60Hz"],
                "electricalInlet": Electricity_240V_60HzInletConnectionPoint,
                "electricalOutlet": Electricity_240V_60HzOutletConnectionPoint,
                "hasMaxRange": Value(
                    20, hasQuantityKind=quantitykind.ElectricCurrent, unit=unit.A
                ),
            },
        },
        # other properties could go there... ?
    }
    elc_panel = DistributionPanel(
        label="P-1",
        comment="Electrical panel full of breakers. 120V-240VAC 60Hz",
        config=distributionpanel_template,
    )

    return elc_panel


def test_turtle_file():
    dump()
    result = turtle()
    print(result)


if __name__ == "__main__":
    panel = test_create_electricalpaneldevice()
    # panel2 = test_create_emptyelectricalpaneldevice()
    result = turtle()
    with open("test_device-006_results.ttl", "w") as file:
        file.write(result)
    print("Check file : test_device-006_results.ttl")
    print(result)
    graph = get_datagraph()
