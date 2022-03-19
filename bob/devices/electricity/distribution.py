from re import S, sub
from rdflib import URIRef, Literal

from bob.property import QuantifiableObservableProperty
from ...core import s223, p223, enum, Device, quantitykind, unit, Medium
from ...connections.electricity import (
    Electricity,
    ElectricalConnection,
    ElectricalSystemConnectionPoint,
    ElectricalConnection,
    ElectricalConnectionPoint,
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    Electricity_120V_240V_60HzConnection,
    Electricity_120V_240V_60HzInletConnectionPoint,
    Electricity_120V_60HzConnection,
    Electricity_120V_60HzInletConnectionPoint,
    Electricity_120V_60HzOutletConnectionPoint,
    Electricity_208V_60HzInletConnectionPoint,
    Electricity_208V_60HzOutletConnectionPoint,
    Electricity_240V_60HzConnection,
    Electricity_240V_60HzOutletConnectionPoint,
    Electricity_240V_60HzInletConnectionPoint,
    Electricity_277V_60HzInletConnectionPoint,
    Electricity_277V_60HzOutletConnectionPoint,
    Electricity_347V_60HzConnection,
    Electricity_347V_60HzConnectionPoint,
    Electricity_347V_60HzInletConnectionPoint,
    Electricity_347V_60HzOutletConnectionPoint,
    Electricity_480V_60HzInletConnectionPoint,
    Electricity_480V_60HzOutletConnectionPoint,
    Electricity_575V_60HzConnection,
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
)
from typing import Dict, Any
from ...sensor import define_sensors
from .. import contains_devices_list

__namespace__ = p223


# class Main(ElectricalConnectionPoint):
##    """
#    Source of the building
###    """
#    hasMedium: Medium


class Transformer(Device):
    node_type = p223.ElectricalTransformer
    hasPower: Literal

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
    node_type = p223.ElectricalDistributionPanel
    manufacturer: str
    modelNumber: str
    hasNumberOfCircuits: QuantifiableObservableProperty

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getitem__(self, name: str) -> Any:
        for each in self._breakers:
            if each.label == name:
                return each
        for each in self._sensors:
            if each.label == name:
                return each


class SinglePhaseDistributionPanel(DistributionPanel):
    manufacturer: str
    modelNumber: str
    hasNumberOfCircuits: QuantifiableObservableProperty
    # Bus Bar
    _cross_ref = {
        "120_240": (
            Electricity_120V_60HzConnection,
            Electricity_120V_60HzConnection,
            Electricity_240V_60HzConnection,
        ),
        "240": (
            Electricity_120V_60HzConnection,
            Electricity_120V_60HzConnection,
            Electricity_240V_60HzConnection,
        ),
    }

    def __init__(self, config: Dict = None, **kwargs):
        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        sensors = define_sensors(config)
        circuit_breakers, device_kwargs = contains_devices_list(config, **kwargs)
        voltage = str(device_kwargs.pop("voltage"))
        _classes = self._cross_ref[voltage]
        _electricalBusA, _electricalBusB, _electricalBusAB = _classes

        super().__init__(**device_kwargs)

        self.electricalBusA = _electricalBusA(label=f"{self.label}.electricalBusA")
        self.electricalBusB = _electricalBusB(label=f"{self.label}.electricalBusB")
        self.electricalBusAB = _electricalBusAB(label=f"{self.label}.electricalBusAB")
        self._breakers = circuit_breakers
        self._sensors = sensors

        for sensor in sensors:
            self > sensor
        for circuit_breaker in circuit_breakers:
            self > circuit_breaker
            if isinstance(circuit_breaker, TwoPolesMainCircuitBreaker):
                circuit_breaker.electricalOutletA >> self.electricalBusA
                circuit_breaker.electricalOutletB >> self.electricalBusB
                circuit_breaker.electricalOutlet >> self.electricalBusAB
            elif isinstance(circuit_breaker, TwoPolesCircuitBreaker):
                self.electricalBusAB >> circuit_breaker
            elif isinstance(circuit_breaker, SinglePoleCircuitBreaker):
                if circuit_breaker._bus_bar in ["A", "odd"]:
                    self.electricalBusA >> circuit_breaker
                else:
                    self.electricalBusB >> circuit_breaker


class ThreePhasesDistributionPanel(DistributionPanel):
    manufacturer: str
    modelNumber: str
    hasNumberOfCircuits: QuantifiableObservableProperty

    # Bus Bar
    _cross_ref = {
        #'208': (Electricity_208V_60HzInletConnectionPoint, Electricity_120V_60HzOutletConnectionPoint, Electricity_120V_60HzOutletConnectionPoint, Electricity_208V_60HzOutletConnectionPoint),
        "575": (
            Electricity_347V_60HzConnection,
            Electricity_347V_60HzConnection,
            Electricity_347V_60HzConnection,
            Electricity_575V_60HzConnection,
        ),
        "600": (
            Electricity_347V_60HzConnection,
            Electricity_347V_60HzConnection,
            Electricity_347V_60HzConnection,
            Electricity_575V_60HzConnection,
        ),
    }

    def __init__(self, config: Dict = None, **kwargs):

        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        sensors = define_sensors(config)
        circuit_breakers, device_kwargs = contains_devices_list(config, **kwargs)
        try:
            voltage = str(device_kwargs.pop("voltage"))
            _classes = self._cross_ref[voltage]
            (
                _electricalBusA,
                _electricalBusB,
                _electricalBusC,
                _electricalBusABC,
            ) = _classes
        except KeyError:
            raise ValueError("You must provide electricalInlet and electricalOutlet")

        super().__init__(**device_kwargs)

        self.electricalBusA = _electricalBusA(label=f"{self.label}.electricalBusA")
        self.electricalBusB = _electricalBusB(label=f"{self.label}.electricalBusB")
        self.electricalBusC = _electricalBusC(label=f"{self.label}.electricalBusC")
        self.electricalBusABC = _electricalBusABC(
            label=f"{self.label}.electricalBusABC"
        )
        self._breakers = circuit_breakers
        self._sensors = sensors
        for sensor in sensors:
            self > sensor
        for circuit_breaker in circuit_breakers:

            self > circuit_breaker

            if isinstance(circuit_breaker, ThreePolesMainCircuitBreaker):
                circuit_breaker.electricalOutletA >> self.electricalBusA
                circuit_breaker.electricalOutletB >> self.electricalBusB
                circuit_breaker.electricalOutletC >> self.electricalBusC
                circuit_breaker.electricalOutlet >> self.electricalBusABC
            elif isinstance(circuit_breaker, ThreePolesCircuitBreaker):
                self.electricalBusABC >> circuit_breaker
            elif isinstance(circuit_breaker, SinglePoleCircuitBreaker):
                if circuit_breaker._bus_bar == "A":
                    self.electricalBusA >> circuit_breaker
                elif circuit_breaker._bus_bar == "B":
                    self.electricalBusB >> circuit_breaker
                else:
                    self.electricalBusC >> circuit_breaker


class CircuitBreaker(Device):
    node_type = p223.ElectricalCircuitBreaker
    # electricalInlet: ElectricalInletConnectionPoint
    # electricalOutlet: ElectricalOutletConnectionPoint
    hasMaxRange: QuantifiableObservableProperty

    def __init__(self, **kwargs):
        amps = kwargs.pop("amps")
        super().__init__(**kwargs)
        self.hasMaxRange = QuantifiableObservableProperty(
            amps,
            hasQuantityKind=quantitykind.ElectricCurrent,
            unit=unit.A,
            label="Current rating of breaker",
        )


class SinglePoleCircuitBreaker(CircuitBreaker):
    """
    One inlet and one outlet
    hasMaxRange = current max of breaker
    A rule could check inlet and outlet are same class
    """

    _cross_ref = {
        "120": (
            Electricity_120V_60HzInletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
        ),
        "277": (
            Electricity_277V_60HzInletConnectionPoint,
            Electricity_277V_60HzOutletConnectionPoint,
        ),
        "347": (
            Electricity_347V_60HzInletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, **kwargs):
        voltage = str(kwargs.pop("voltage"))
        _classes = self._cross_ref[voltage]
        self._bus_bar = str(kwargs.pop("bus_bar"))
        try:
            _electricalInlet, _electricalOutlet = _classes
        except KeyError:
            raise ValueError("You must provide electricalInlet and electricalOutlet")
        super().__init__(**kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


class TwoPolesCircuitBreaker(CircuitBreaker):
    """
    One electrical Inlet because when plugin the breaker
    in the panel, you get no choice. Both poles are connected
    at the same time. Electricity is fed from 2 bus bar (2 x 120V)
    The electrical Outlet is a little different. You could potentially
    use only 1 pole (347V heating or light for example)
    So 3 choices are possible pole A, pole B or pole A-B
    """

    _cross_ref = {
        "240": (
            Electricity_240V_60HzInletConnectionPoint,
            Electricity_240V_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, **kwargs):
        voltage = str(kwargs.pop("voltage"))
        _classes = self._cross_ref[voltage]
        try:
            (_electricalInlet, _electricalOutlet) = _classes
        except KeyError:
            raise ValueError("You must provide electricalInlet and electricalOutlet")
        super().__init__(**kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


class TwoPolesMainCircuitBreaker(CircuitBreaker):
    """
    A 2 poles Main circuit breaker is modeled differently as I
    wanted to illustrate the fact that it will be connected to
    the 2 bus bars in the panel (A & B) and will also be connected
    to AB. It is really a modeling trick.
    """

    # _cross_ref will map the right voltages to input and bus bars
    _cross_ref = {
        "120_240": (
            Electricity_120V_240V_60HzInletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_240V_60HzOutletConnectionPoint,
        ),
        "240": (
            Electricity_240V_60HzInletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_240V_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, **kwargs):
        voltage = str(kwargs.pop("voltage"))
        _classes = self._cross_ref[voltage]
        try:
            (
                _electricalInlet,
                _electricalOutletA,
                _electricalOutletB,
                _electricalOutlet,
            ) = _classes
        except KeyError:
            raise ValueError("You must provide electricalInlet and electricalOutlet")
        super().__init__(**kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutletA = _electricalOutletA(
            self, label=f"{self.label}.electricalOutlet_LineA_Neutral"
        )
        self.electricalOutletB = _electricalOutletB(
            self, label=f"{self.label}.electricalOutlet_LineB_Neutral"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet_LineA_LineB"
        )


class ThreePolesCircuitBreaker(CircuitBreaker):
    """
    One electrical Inlet because when plugin the breaker
    in the panel, you get no choice. Both poles are connected
    at the same time. Electricity is fed from 2 bus bar (2 x 120V)
    The electrical Outlet is a little different. You could potentially
    use only 1 pole (347V heating or light for example)
    So 3 choices are possible pole A, pole B or pole A-B
    """

    _cross_ref = {
        "208": (
            Electricity_208V_60HzInletConnectionPoint,
            Electricity_208V_60HzOutletConnectionPoint,
        ),
        "480": (
            Electricity_480V_60HzInletConnectionPoint,
            Electricity_480V_60HzOutletConnectionPoint,
        ),
        "575": (
            Electricity_575V_60HzInletConnectionPoint,
            Electricity_575V_60HzOutletConnectionPoint,
        ),
        "600": (
            Electricity_575V_60HzInletConnectionPoint,
            Electricity_575V_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, **kwargs):
        voltage = str(kwargs.pop("voltage"))
        _classes = self._cross_ref[voltage]
        try:
            _electricalInlet, _electricalOutlet = _classes
        except KeyError:
            raise ValueError("You must provide electricalInlet and electricalOutlet")
        super().__init__(**kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )

        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


class ThreePolesMainCircuitBreaker(CircuitBreaker):
    """
    One electrical Inlet because when plugin the breaker
    in the panel, you get no choice. Three poles are connected
    at the same time. Electricity is fed from 3 bus bar (3 x 347V to neutral for example)

    Code do not allow to use only one pole of a 3phase breaker. So
    this model is just a trick so we can feed 3 bus bar (connect) inside the panel.
    If not, we would have 3 connections coming from vaccuum of space.

    """

    # _cross_ref will map the right voltages to input and bus bars
    _cross_ref = {
        "208": (
            Electricity_208V_60HzInletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_208V_60HzOutletConnectionPoint,
        ),
        "480": (
            Electricity_480V_60HzInletConnectionPoint,
            Electricity_277V_60HzOutletConnectionPoint,
            Electricity_277V_60HzOutletConnectionPoint,
            Electricity_277V_60HzOutletConnectionPoint,
            Electricity_480V_60HzOutletConnectionPoint,
        ),
        "575": (
            Electricity_575V_60HzInletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_575V_60HzOutletConnectionPoint,
        ),
        "600": (
            Electricity_575V_60HzInletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_575V_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, **kwargs):
        voltage = str(kwargs.pop("voltage"))
        _classes = self._cross_ref[voltage]
        try:
            (
                _electricalInlet,
                _electricalOutletA,
                _electricalOutletB,
                _electricalOutletC,
                _electricalOutlet,
            ) = _classes
        except KeyError:
            raise ValueError("You must provide electricalInlet and electricalOutlet")
        super().__init__(**kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutletA = _electricalOutletA(
            self, label=f"{self.label}.electricalOutletA"
        )
        self.electricalOutletB = _electricalOutletB(
            self, label=f"{self.label}.electricalOutletB"
        )
        self.electricalOutletC = _electricalOutletC(
            self, label=f"{self.label}.electricalOutletC"
        )

        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutletABC"
        )


# Define breaker in template
SinglePhasePanel_config = {
    "params": {
        "label": "My Panel",
        "comment": "Description of my panel",
        "voltage": 120_240,
    },
    "sensors": {},
    "contains": {
        ("MainBreaker", TwoPolesMainCircuitBreaker): {
            "comment": "Main breaker of panel",
            "amps": 200,
            "voltage": 240,
        },
        ("CB#1", SinglePoleCircuitBreaker): {
            "comment": "Lights",
            "amps": 15,
            "voltage": 120,
            "bus_bar": "A",
        },
        ("CB#2", TwoPolesCircuitBreaker): {
            "comment": "Heater",
            "amps": 20,
            "voltage": 240,
        },
    },
    # other properties could go there... ?
}

# Define breaker in template
ThreePhasePanel_config = {
    "params": {
        "label": "My Panel",
        "comment": "Description of my panel",
        "voltage": 575,
    },
    "sensors": {},
    "contains": {
        ("MainBreaker", ThreePolesMainCircuitBreaker): {
            "comment": "Main breaker of panel",
            "amps": 200,
            "voltage": 575,
        },
        ("CB#1", SinglePoleCircuitBreaker): {
            "comment": "Lights",
            "amps": 15,
            "voltage": 347,
            "bus_bar": "A",
        },
        ("CB#2", ThreePolesCircuitBreaker): {
            "comment": "Heater",
            "amps": 40,
            "voltage": 575,
        },
    },
    # other properties could go there... ?
}
