from re import S, sub
from rdflib import URIRef

from bob.property import QuantifiableObservableProperty
from ...core import s223, enum, Device, Value, quantitykind, unit, Medium
from ...connections.electricity import (
    Electricity,
    ElectricalConnection,
    ElectricalSystemConnectionPoint,
    ElectricalConnection,
    ElectricalConnectionPoint,
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    Electricity_120V_60HzInletConnectionPoint,
    Electricity_120V_60HzOutletConnectionPoint,
    Electricity_240V_60HzOutletConnectionPoint,
    Electricity_240V_60HzInletConnectionPoint,
)
from typing import Dict
from ...sensor import define_sensors
from .. import contains_devices_list

__namespace__ = s223


# class Main(ElectricalConnectionPoint):
##    """
#    Source of the building
###    """
#    hasMedium: Medium


class Transformer(Device):
    node_type = s223.ElectricalTransformer
    hasPower: Value

    def __init__(self, **kwargs):
        try:
            _electricalInlet = kwargs.pop("electricalInlet")
            _electricalOutlet = kwargs.pop("electricalOutlet")
        except KeyError:
            raise ValueError("You must provide electricalInlet and electricalOutlet")
        super().__init__(**kwargs)
        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


class DistributionPanel(Device):
    # manufacturer: str
    # modelNumber: str
    # hasNumberOfCircuits: Value()
    node_type = s223.ElectricalDistributionPanel

    def __init__(self, config: Dict = None, **kwargs):
        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        sensors = define_sensors(config)
        circuit_breakers, device_kwargs = contains_devices_list(config, **kwargs)
        try:
            _electricalInlet = device_kwargs.pop("electricalInlet")
            _electricalOutletA = device_kwargs.pop("electricalOutletA")
            _electricalOutletB = device_kwargs.pop("electricalOutletB")
        except KeyError:
            raise ValueError("You must provide electricalInlet and electricalOutlet")

        super().__init__(**device_kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutletA = _electricalOutletA(
            self, label=f"{self.label}.electricalOutletA"
        )
        self.electricalOutletB = _electricalOutletB(
            self, label=f"{self.label}.electricalOutletB"
        )

        for sensor in sensors:
            self > sensor
        for circuit_breaker in circuit_breakers:
            self > circuit_breaker
            self >> circuit_breaker


class CircuitBreaker(Device):
    node_type = s223.ElectricalCircuitBreaker
    # electricalInlet: ElectricalInletConnectionPoint
    # electricalOutlet: ElectricalOutletConnectionPoint
    hasMaxRange: QuantifiableObservableProperty

    def __init__(self, **kwargs):
        try:
            _electricalInlet = kwargs.pop("electricalInlet")
            _electricalOutlet = kwargs.pop("electricalOutlet")
        except KeyError:
            raise ValueError("You must provide electricalInlet and electricalOutlet")
        super().__init__(**kwargs)
        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


distributionpanel_template = {
    "params": {
        "label": "Name Of Panel",
        "comment": "Description",
        # "electricalInlet": Electricity_120V_240V_60HzInletConnectionPoint,
        # "electricalOutletA": Electricity_120V_60HzOutletConnectionPoint,
        # "electricalOutletB": Electricity_240V_60HzOutletConnectionPoint,
        # "hasMeasurementLocation": Connection,
    },
    "sensors": {},
    "contains": {
        ("CircBreaker_120_#1", CircuitBreaker): {
            "comment": "Office lights #1",
            "electricalInlet": Electricity_120V_60HzInletConnectionPoint,
            "electricalOutlet": Electricity_120V_60HzOutletConnectionPoint,
            "hasMaxRange": QuantifiableObservableProperty(
                15, hasQuantityKind=quantitykind.ElectricCurrent, unit=unit.A
            ),
        },
        ("CircBreaker_240_#2", CircuitBreaker): {
            "comment": "Heating Room #1",
            "electricalInlet": Electricity_240V_60HzInletConnectionPoint,
            "electricalOutlet": Electricity_240V_60HzOutletConnectionPoint,
            "hasMaxRange": QuantifiableObservableProperty(
                20, hasQuantityKind=quantitykind.ElectricCurrent, unit=unit.A
            ),
        },
    },
    # other properties could go there... ?
}
