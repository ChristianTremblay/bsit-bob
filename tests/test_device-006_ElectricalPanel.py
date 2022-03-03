from bob.core import (
    bind_model_namespace,
    quantitykind,
    unit,
    dump,
)

from bob.devices.electricity.distribution import DistributionPanel, CircuitBreaker
from bob.connections.electricity import (
    Electricity_120V_60HzInletConnectionPoint,
    Electricity_120V_60HzOutletConnectionPoint,
    Electricity_240V_60HzInletConnectionPoint,
    Electricity_240V_60HzOutletConnectionPoint,
    Electricity_120V_240V_60HzInletConnectionPoint,
)
from bob.property import QuantifiableObservableProperty

from pathlib import Path

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


distributionpanel1_template = {
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
elc_panel1 = DistributionPanel(
    label="P-1",
    comment="Electrical panel full of breakers. 120V-240VAC 60Hz",
    config=distributionpanel1_template,
)

distributionpanel2_template = {
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
            "electricalInlet": Electricity_120V_60HzInletConnectionPoint,
            "electricalOutlet": Electricity_120V_60HzOutletConnectionPoint,
            "hasMaxRange": QuantifiableObservableProperty(
                15,
                hasQuantityKind=quantitykind.ElectricCurrent,
                unit=unit.A,
                label="Current rating of breaker",
            ),
        },
        ("CircBreaker_240_#2", CircuitBreaker): {
            "comment": "Heating Room #1",
            "electricalInlet": Electricity_240V_60HzInletConnectionPoint,
            "electricalOutlet": Electricity_240V_60HzOutletConnectionPoint,
            "hasMaxRange": QuantifiableObservableProperty(
                20,
                hasQuantityKind=quantitykind.ElectricCurrent,
                unit=unit.A,
                label="Current rating of breaker",
            ),
        },
    },
    # other properties could go there... ?
}
elc_panel2 = DistributionPanel(
    label="P-1",
    comment="Electrical panel full of breakers. 120V-240VAC 60Hz",
    config=distributionpanel2_template,
)

dump()
