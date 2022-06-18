from typing import Dict

from rdflib import Literal

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
    Electricity_120V_60HzConnection,
    Electricity_120V_60HzInletConnectionPoint,
    Electricity_120V_60HzOutletConnectionPoint,
    Electricity_120V_240V_60HzConnection,
    Electricity_120V_240V_60HzInletConnectionPoint,
    Electricity_208V_60HzInletConnectionPoint,
    Electricity_208V_60HzOutletConnectionPoint,
    Electricity_240V_60HzConnection,
    Electricity_240V_60HzInletConnectionPoint,
    Electricity_240V_60HzOutletConnectionPoint,
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
from ...core import Device, bob, p223, quantitykind, unit

_namespace = bob


class Transformer(Device):
    _class_iri = p223.ElectricalTransformer
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


class SinglePhaseDistributionPanel(Device):
    _class_iri = p223.ElectricalDistributionPanel
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

        self.electricalBusA = _electricalBusA(label=f"{self.label}.electricalBusA")
        self.electricalBusB = _electricalBusB(label=f"{self.label}.electricalBusB")
        self.electricalBusAB = _electricalBusAB(label=f"{self.label}.electricalBusAB")

        for circuit_breaker in getattr(self, "_devices", []):
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


class ThreePhaseDistributionPanel(Device):
    _class_iri = p223.ElectricalDistributionPanel
    manufacturer: str
    modelNumber: str
    number_of_circuits: QuantifiableObservableProperty

    # Bus Bar
    _cross_ref = {
        "208": (
            Electricity_208V_60HzInletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
            Electricity_208V_60HzOutletConnectionPoint,
        ),
        "575": (
            (Electricity_347V_60HzConnection),
            (Electricity_347V_60HzConnection),
            (Electricity_347V_60HzConnection),
            (Electricity_575V_60HzConnection),
        ),
        "600": (
            (Electricity_347V_60HzConnection),
            (Electricity_347V_60HzConnection),
            (Electricity_347V_60HzConnection),
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
            _electricalBusABC,
        ) = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

        self.electricalBusA = _electricalBusA(label=f"{self.label}.electricalBusA")
        self.electricalBusB = _electricalBusB(label=f"{self.label}.electricalBusB")
        self.electricalBusC = _electricalBusC(label=f"{self.label}.electricalBusC")
        self.electricalBusABC = _electricalBusABC(
            label=f"{self.label}.electricalBusABC"
        )

        for circuit_breaker in getattr(self, "_devices", []):
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
    _class_iri = p223.ElectricalCircuitBreaker
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

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        voltage = kwargs.pop("voltage")

        # look up the connection point classes
        (
            _electricalInlet,
            _electricalOutletA,
            _electricalOutletB,
            _electricalOutletC,
            _electricalOutlet,
        ) = self._cross_ref[str(voltage)]

        super().__init__(config, **kwargs)

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
    "devices": {
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
    "devices": {
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
