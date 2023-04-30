from typing import Dict

from rdflib import Literal

from bob.enum import ElectricalPhaseIdentifier
from bob.properties import ElectricPowerkW
from bob.properties.electricity import Amps
from bob.property import QuantifiableObservableProperty

from ...connections.electricity import (
    ElectricalConnection,
    ElectricalConnectionPoint,
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    ElectricalSystemConnectionPoint,
    Electricity,
    Electricity_120V_208V_240V_60HzInletConnectionPoint,
    Electricity_120V_60HzConnection,
    Electricity_120V_60HzInletConnectionPoint,
    Electricity_120V_60HzOutletConnectionPoint,
    Electricity_120V_240V_60HzConnection,
    Electricity_120V_240V_60HzInletConnectionPoint,
    Electricity_208V1Ph_60HzConnection,
    Electricity_208V1Ph_60HzInletConnectionPoint,
    Electricity_208V1Ph_60HzOutletConnectionPoint,
    Electricity_208V_60HzConnection,
    Electricity_208V_60HzInletConnectionPoint,
    Electricity_208V_60HzOutletConnectionPoint,
    Electricity_240V3Ph_60HzConnection,
    Electricity_240V3Ph_60HzInletConnectionPoint,
    Electricity_240V3Ph_60HzOutletConnectionPoint,
    Electricity_240V_60HzConnection,
    Electricity_240V_60HzInletConnectionPoint,
    Electricity_240V_60HzOutletConnectionPoint,
    Electricity_277V_60HzInletConnectionPoint,
    Electricity_277V_60HzOutletConnectionPoint,
    Electricity_347V_60HzConnection,
    Electricity_347V_60HzInletConnectionPoint,
    Electricity_347V_60HzOutletConnectionPoint,
    Electricity_480V1Ph_60HzInletConnectionPoint,
    Electricity_480V1Ph_60HzOutletConnectionPoint,
    Electricity_480V_60HzInletConnectionPoint,
    Electricity_480V_60HzOutletConnectionPoint,
    Electricity_575V_60HzConnection,
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
    Electricity_600V1Ph_60HzConnection,
    Electricity_600V1Ph_60HzInletConnectionPoint,
    Electricity_600V1Ph_60HzOutletConnectionPoint,
)
from ...core import BOB, P223, QUANTITYKIND, UNIT, Equipment

_namespace = BOB


class Transformer(Equipment):
    _class_iri = P223.ElectricalTransformer
    hasPower: ElectricPowerkW

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        _electricalInlet = kwargs.pop("electricalInlet")
        _electricalOutlet = kwargs.pop("electricalOutlet")

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


class SinglePhaseDistributionPanel(Equipment):
    _class_iri = P223.ElectricalDistributionPanel
    manufacturer: str
    modelNumber: str
    number_of_circuits: QuantifiableObservableProperty

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

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        _electricalBusA, _electricalBusB, _electricalBusAB = self._cross_ref[
            str(voltage)
        ]

        super().__init__(config, **kwargs)

        self.electricalBusA = (
            _electricalBusA(label=f"{self.label}.electricalBusA")
            + ElectricalPhaseIdentifier.A
        )
        self.electricalBusB = (
            _electricalBusB(label=f"{self.label}.electricalBusB")
            + ElectricalPhaseIdentifier.B
        )
        self.electricalBusAB = (
            _electricalBusAB(label=f"{self.label}.electricalBusAB")
            + ElectricalPhaseIdentifier.AB
        )

        for _lit, circuit_breaker in self._contents.items():
            if isinstance(circuit_breaker, TwoPolesMainCircuitBreaker):
                circuit_breaker.electricalOutletA >> self.electricalBusA
                circuit_breaker.electricalOutletB >> self.electricalBusB
                circuit_breaker.electricalOutlet >> self.electricalBusAB
            elif isinstance(circuit_breaker, TwoPolesCircuitBreaker):
                self.electricalBusAB >> circuit_breaker
            elif isinstance(circuit_breaker, SinglePoleCircuitBreaker):
                if circuit_breaker._bus_bar in ("A", "odd"):
                    self.electricalBusA >> circuit_breaker
                else:
                    self.electricalBusB >> circuit_breaker
            elif isinstance(circuit_breaker, TandemSinglePoleCircuitBreaker):
                if circuit_breaker._bus_bar in ("A", "odd"):
                    self.electricalBusA >> circuit_breaker
                else:
                    self.electricalBusB >> circuit_breaker


class ThreePhaseDistributionPanel(Equipment):
    _class_iri = P223.ElectricalDistributionPanel
    manufacturer: str
    modelNumber: str
    number_of_circuits: QuantifiableObservableProperty

    # Bus Bar
    _cross_ref = {
        "HighLeg": (
            Electricity_120V_60HzConnection,
            Electricity_120V_60HzConnection,
            Electricity_208V1Ph_60HzConnection,
            Electricity_240V_60HzConnection,
            Electricity_240V_60HzConnection,
            Electricity_240V_60HzConnection,
            Electricity_240V3Ph_60HzConnection,
        ),
        "208": (
            Electricity_120V_60HzConnection,
            Electricity_120V_60HzConnection,
            Electricity_120V_60HzConnection,
            Electricity_208V1Ph_60HzConnection,
            Electricity_208V1Ph_60HzConnection,
            Electricity_208V1Ph_60HzConnection,
            Electricity_208V_60HzConnection,
        ),
        "575": (
            (Electricity_347V_60HzConnection),
            (Electricity_347V_60HzConnection),
            (Electricity_347V_60HzConnection),
            Electricity_600V1Ph_60HzConnection,
            (Electricity_600V1Ph_60HzConnection),
            (Electricity_600V1Ph_60HzConnection),
            (Electricity_575V_60HzConnection),
        ),
        "600": (
            (Electricity_347V_60HzConnection),
            (Electricity_347V_60HzConnection),
            (Electricity_347V_60HzConnection),
            Electricity_600V1Ph_60HzConnection,
            (Electricity_600V1Ph_60HzConnection),
            (Electricity_600V1Ph_60HzConnection),
            (Electricity_575V_60HzConnection),
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        (
            _electricalBusA,
            _electricalBusB,
            _electricalBusC,
            _electricalBusAB,
            _electricalBusBC,
            _electricalBusCA,
            _electricalBusABC,
        ) = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

        self.electricalBusA = _electricalBusA(label=f"{self.label}.electricalBusA")
        self.electricalBusB = _electricalBusB(label=f"{self.label}.electricalBusB")
        self.electricalBusC = _electricalBusC(label=f"{self.label}.electricalBusC")
        self.electricalBusAB = _electricalBusAB(label=f"{self.label}.electricalBusAB")
        self.electricalBusBC = _electricalBusBC(label=f"{self.label}.electricalBusBC")
        self.electricalBusCA = _electricalBusCA(label=f"{self.label}.electricalBusCA")
        self.electricalBusABC = _electricalBusABC(
            label=f"{self.label}.electricalBusABC"
        )

        self.electricalBusA + ElectricalPhaseIdentifier.A
        self.electricalBusB + ElectricalPhaseIdentifier.B
        self.electricalBusC + ElectricalPhaseIdentifier.C
        self.electricalBusAB + ElectricalPhaseIdentifier.AB
        self.electricalBusBC + ElectricalPhaseIdentifier.BC
        self.electricalBusCA + ElectricalPhaseIdentifier.CA
        self.electricalBusABC + ElectricalPhaseIdentifier.ABC

        for lit, circuit_breaker in self._contents.items():
            print(circuit_breaker)
            if isinstance(circuit_breaker, ThreePolesMainCircuitBreaker):
                print("connections")
                circuit_breaker.electricalOutletA >> self.electricalBusA
                circuit_breaker.electricalOutletB >> self.electricalBusB
                circuit_breaker.electricalOutletC >> self.electricalBusC
                circuit_breaker.electricalOutletAB >> self.electricalBusAB
                circuit_breaker.electricalOutletBC >> self.electricalBusBC
                circuit_breaker.electricalOutletCA >> self.electricalBusCA
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
            elif isinstance(circuit_breaker, TwoPolesCircuitBreaker):
                if circuit_breaker._bus_bar == "AB":
                    self.electricalBusAB >> circuit_breaker
                elif circuit_breaker._bus_bar == "BC":
                    self.electricalBusBC >> circuit_breaker
                else:
                    self.electricalBusCA >> circuit_breaker


class CircuitBreaker(Equipment):
    _class_iri = P223.ElectricalCircuitBreaker
    # electricalInlet: ElectricalInletConnectionPoint
    # electricalOutlet: ElectricalOutletConnectionPoint
    currentRating: Amps

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        amps = kwargs.pop("amps")

        super().__init__(config, **kwargs)

        self.currentRating = Amps(amps, label="Current rating of breaker")


class SinglePoleCircuitBreaker(CircuitBreaker):
    """
    One inlet and one outlet
    hasMaxRange = current max of breaker
    A rule could check inlet and outlet are same class

    208V single pole available in the High Leg Configuration
    """

    _cross_ref = {
        "120": (
            Electricity_120V_60HzInletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
        ),
        "208": (
            Electricity_208V1Ph_60HzInletConnectionPoint,
            Electricity_208V1Ph_60HzOutletConnectionPoint,
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

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")
        self._bus_bar = kwargs.pop("bus_bar")

        # look up the inlet and outlet classes
        _electricalInlet, _electricalOutlet = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutlet = _electricalOutlet(
            self, label=f"{self.label}.electricalOutlet"
        )


class TandemSinglePoleCircuitBreaker(CircuitBreaker):
    """
    One inlet and two outlets, also known as Twin breakers
    hasMaxRange = current max of breaker
    A rule could check inlet and outlets are same class
    """

    _cross_ref = {
        "120": (
            Electricity_120V_60HzInletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")
        self._bus_bar = kwargs.pop("bus_bar")

        # look up the inlet and outlet classes
        _electricalInlet, _electricalOutletA, _electricalOutletB = self._cross_ref[
            str(voltage)
        ]

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutletA = _electricalOutletA(
            self, label=f"{self.label}.electricalOutlet"
        )
        self.electricalOutletB = _electricalOutletB(
            self, label=f"{self.label}.electricalOutlet"
        )


class TwoPolesCircuitBreaker(CircuitBreaker):
    """
    One electrical Inlet because when plugin the breaker
    in the panel, you get no choice. Both poles are connected
    at the same time. Electricity is fed from 2 bus bar (2 x 120V)
    Could also use 208V instead of 240V...
    """

    _cross_ref = {
        "208": (
            Electricity_208V1Ph_60HzInletConnectionPoint,
            Electricity_208V1Ph_60HzOutletConnectionPoint,
        ),
        "240": (
            Electricity_240V_60HzInletConnectionPoint,
            Electricity_240V_60HzOutletConnectionPoint,
        ),
        "480": (
            Electricity_480V1Ph_60HzInletConnectionPoint,
            Electricity_480V1Ph_60HzOutletConnectionPoint,
        ),
        "600": (
            Electricity_600V1Ph_60HzInletConnectionPoint,
            Electricity_600V1Ph_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")
        self._bus_bar = kwargs.pop("bus_bar", "AB")

        # look up the connection point classes
        _electricalInlet, _electricalOutlet = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

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

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        (
            _electricalInlet,
            _electricalOutletA,
            _electricalOutletB,
            _electricalOutlet,
        ) = self._cross_ref[str(voltage)]

        super().__init__(**kwargs)

        self.electricalInlet = (
            _electricalInlet(self, label=f"{self.label}.electricalInlet")
            + ElectricalPhaseIdentifier.AB
        )
        self.electricalOutletA = (
            _electricalOutletA(
                self, label=f"{self.label}.electricalOutlet_LineA_Neutral"
            )
            + ElectricalPhaseIdentifier.A
        )
        self.electricalOutletB = (
            _electricalOutletB(
                self, label=f"{self.label}.electricalOutlet_LineB_Neutral"
            )
            + ElectricalPhaseIdentifier.B
        )
        self.electricalOutlet = (
            _electricalOutlet(self, label=f"{self.label}.electricalOutlet_LineA_LineB")
            + ElectricalPhaseIdentifier.AB
        )


class ThreePolesCircuitBreaker(CircuitBreaker):
    """
    One electrical Inlet because when plugin the breaker
    in the panel, you get no choice. Three poles are connected
    at the same time. Electricity is fed from 3 bus bars
    """

    _cross_ref = {
        "208": (
            Electricity_208V_60HzInletConnectionPoint,
            Electricity_208V_60HzOutletConnectionPoint,
        ),
        "240": (
            Electricity_240V3Ph_60HzInletConnectionPoint,
            Electricity_240V3Ph_60HzOutletConnectionPoint,
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

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        _electricalInlet, _electricalOutlet = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

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
        "HighLeg": (
            Electricity_120V_208V_240V_60HzInletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_208V1Ph_60HzOutletConnectionPoint,
            Electricity_240V_60HzOutletConnectionPoint,
            Electricity_240V_60HzOutletConnectionPoint,
            Electricity_240V_60HzOutletConnectionPoint,
            Electricity_240V3Ph_60HzOutletConnectionPoint,
        ),
        "208": (
            Electricity_208V_60HzInletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_208V1Ph_60HzOutletConnectionPoint,
            Electricity_208V1Ph_60HzOutletConnectionPoint,
            Electricity_208V1Ph_60HzOutletConnectionPoint,
            Electricity_208V_60HzOutletConnectionPoint,
        ),
        "480": (
            Electricity_480V_60HzInletConnectionPoint,
            Electricity_277V_60HzOutletConnectionPoint,
            Electricity_277V_60HzOutletConnectionPoint,
            Electricity_277V_60HzOutletConnectionPoint,
            Electricity_480V1Ph_60HzOutletConnectionPoint,
            Electricity_480V1Ph_60HzOutletConnectionPoint,
            Electricity_480V1Ph_60HzOutletConnectionPoint,
            Electricity_480V_60HzOutletConnectionPoint,
        ),
        "575": (
            Electricity_575V_60HzInletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_600V1Ph_60HzOutletConnectionPoint,
            Electricity_600V1Ph_60HzOutletConnectionPoint,
            Electricity_600V1Ph_60HzOutletConnectionPoint,
            Electricity_575V_60HzOutletConnectionPoint,
        ),
        "600": (
            Electricity_575V_60HzInletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
            Electricity_600V1Ph_60HzOutletConnectionPoint,
            Electricity_600V1Ph_60HzOutletConnectionPoint,
            Electricity_600V1Ph_60HzOutletConnectionPoint,
            Electricity_575V_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        (
            _electricalInlet,
            _electricalOutletA,
            _electricalOutletB,
            _electricalOutletC,
            _electricalOutletAB,
            _electricalOutletBC,
            _electricalOutletCA,
            _electricalOutlet,
        ) = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

        self.electricalInlet = _electricalInlet(
            self, label=f"{self.label}.electricalInlet"
        )
        self.electricalOutletA = (
            _electricalOutletA(self, label=f"{self.label}.electricalOutletA")
            + ElectricalPhaseIdentifier.A
        )
        self.electricalOutletB = (
            _electricalOutletB(self, label=f"{self.label}.electricalOutletB")
            + ElectricalPhaseIdentifier.B
        )
        self.electricalOutletC = (
            _electricalOutletC(self, label=f"{self.label}.electricalOutletC")
            + ElectricalPhaseIdentifier.C
        )
        self.electricalOutletAB = (
            _electricalOutletAB(self, label=f"{self.label}.electricalOutletAB")
            + ElectricalPhaseIdentifier.AB
        )
        self.electricalOutletBC = (
            _electricalOutletBC(self, label=f"{self.label}.electricalOutletBC")
            + ElectricalPhaseIdentifier.BC
        )
        self.electricalOutletCA = (
            _electricalOutletCA(self, label=f"{self.label}.electricalOutletCA")
            + ElectricalPhaseIdentifier.CA
        )
        self.electricalOutlet = (
            _electricalOutlet(self, label=f"{self.label}.electricalOutletABC")
            + ElectricalPhaseIdentifier.ABC
        )


# Define breaker in template
SinglePhasePanel_config = {
    "params": {
        "label": "My Panel",
        "comment": "Description of my panel",
        "voltage": 120_240,
    },
    "sensors": {},
    "equipment": {
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
    "equipment": {
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
