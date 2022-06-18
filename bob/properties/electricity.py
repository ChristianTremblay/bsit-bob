from re import L
from typing import Any

from rdflib import URIRef

from ..core import bob, p223, quantitykind, s223, unit
from ..property import QuantifiableObservableProperty

_namespace = bob


class Volts(QuantifiableObservableProperty):
    _node_iri = p223.Volts
    hasQuantityKind = quantitykind.Voltage
    unit = unit.V


class Amps(QuantifiableObservableProperty):
    _node_iri = p223.Amps
    hasQuantityKind = quantitykind.ElectricCurrent
    unit = unit.A


class PowerFactor(QuantifiableObservableProperty):
    _node_iri = p223.PowerFactor
    hasQuantityKind = quantitykind.PowerFactor
    unit = unit.UNITLESS


class Frequency(QuantifiableObservableProperty):
    _node_iri = p223.Frequency
    hasQuantityKind = quantitykind.Frequency
    unit = unit.HZ


class ElectricPower(QuantifiableObservableProperty):
    _node_iri = p223.ElectricPower
    hasQuantityKind = quantitykind.Power
    unit: URIRef
    _supported_units = [
        unit.KiloW,
        unit.W,
        unit.TeraW,
        unit.PicoW,
        unit.NanoW,
        unit.MilliW,
        unit.MicroW,
        unit.MegaW,
        unit.HP_Electric,
        unit.GigaW,
    ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricApparentPower(QuantifiableObservableProperty):
    _node_iri = p223.ElectricApparentPower
    hasQuantityKind = quantitykind.ComplexPower
    unit: URIRef
    _supported_units = [unit["V-A"], unit["KiloV-A"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricReactivePower(QuantifiableObservableProperty):
    _node_iri = p223.ElectricReactivePower
    hasQuantityKind = quantitykind.ReactivePower
    unit: URIRef
    _supported_units = [unit["V-A_Reactive"], unit["KiloV-A_Reactive"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


# Super common....so making a shortcut


class ElectricPowerkW(ElectricPower):
    def __init__(self, **kwargs):
        kwargs["unit"] = unit.KiloW
        super().__init__(**kwargs)


class ElectricPowerW(ElectricPower):
    def __init__(self, **kwargs):
        kwargs["unit"] = unit.W
        super().__init__(**kwargs)


# Energy
class ElectricEnergy(QuantifiableObservableProperty):
    _node_iri = p223.ElectricEnergy
    hasQuantityKind = quantitykind.Energy
    unit: URIRef
    _supported_units = [
        unit["KiloW-HR"],
        unit["W-HR"],
        unit["TeraW-HR"],
        unit["MegaW-HR"],
        unit["GigaW-HR"],
    ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricApparentEnergy(QuantifiableObservableProperty):
    _node_iri = p223.ElectricApparentEnergy
    hasQuantityKind = quantitykind.Energy
    unit: URIRef
    _supported_units = [unit["V-A-HR"], unit["KiloV-A-HR"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricReactiveEnergy(QuantifiableObservableProperty):
    _node_iri = p223.ElectricReactiveEnergy
    hasQuantityKind = quantitykind.Energy
    unit: URIRef
    _supported_units = [unit["V-A_Reactive-HR"], unit["KiloV-A_Reactive-HR"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)
