from re import L
from typing import Any

from rdflib import URIRef

from ..core import BOB, P223, QUANTITYKIND, S223, UNIT
from ..property import QuantifiableObservableProperty

_namespace = BOB


class Volts(QuantifiableObservableProperty):
    _node_iri = P223.Volts
    hasQuantityKind = QUANTITYKIND.Voltage
    unit = UNIT.V


class Amps(QuantifiableObservableProperty):
    _node_iri = P223.Amps
    hasQuantityKind = QUANTITYKIND.ElectricCurrent
    unit = UNIT.A


class PowerFactor(QuantifiableObservableProperty):
    _node_iri = P223.PowerFactor
    hasQuantityKind = QUANTITYKIND.PowerFactor
    unit = UNIT.UNITLESS


class Frequency(QuantifiableObservableProperty):
    _node_iri = P223.Frequency
    hasQuantityKind = QUANTITYKIND.Frequency
    unit = UNIT.HZ


class ElectricPower(QuantifiableObservableProperty):
    _node_iri = P223.ElectricPower
    hasQuantityKind = QUANTITYKIND.Power
    unit: URIRef
    _supported_units = [
        UNIT.KiloW,
        UNIT.W,
        UNIT.TeraW,
        UNIT.PicoW,
        UNIT.NanoW,
        UNIT.MilliW,
        UNIT.MicroW,
        UNIT.MegaW,
        UNIT.HP_Electric,
        UNIT.GigaW,
    ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricApparentPower(QuantifiableObservableProperty):
    _node_iri = P223.ElectricApparentPower
    hasQuantityKind = QUANTITYKIND.ComplexPower
    unit: URIRef
    _supported_units = [UNIT["V-A"], UNIT["KiloV-A"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricReactivePower(QuantifiableObservableProperty):
    _node_iri = P223.ElectricReactivePower
    hasQuantityKind = QUANTITYKIND.ReactivePower
    unit: URIRef
    _supported_units = [UNIT["V-A_Reactive"], UNIT["KiloV-A_Reactive"]]

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
        kwargs["unit"] = UNIT.KiloW
        super().__init__(**kwargs)


class ElectricPowerW(ElectricPower):
    def __init__(self, **kwargs):
        kwargs["unit"] = UNIT.W
        super().__init__(**kwargs)


# Energy
class ElectricEnergy(QuantifiableObservableProperty):
    _node_iri = P223.ElectricEnergy
    hasQuantityKind = QUANTITYKIND.Energy
    unit: URIRef
    _supported_units = [
        UNIT["KiloW-HR"],
        UNIT["W-HR"],
        UNIT["TeraW-HR"],
        UNIT["MegaW-HR"],
        UNIT["GigaW-HR"],
    ]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricApparentEnergy(QuantifiableObservableProperty):
    _node_iri = P223.ElectricApparentEnergy
    hasQuantityKind = QUANTITYKIND.Energy
    unit: URIRef
    _supported_units = [UNIT["V-A-HR"], UNIT["KiloV-A-HR"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)


class ElectricReactiveEnergy(QuantifiableObservableProperty):
    _node_iri = P223.ElectricReactiveEnergy
    hasQuantityKind = QUANTITYKIND.Energy
    unit: URIRef
    _supported_units = [UNIT["V-A_Reactive-HR"], UNIT["KiloV-A_Reactive-HR"]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not ("unit" in kwargs and kwargs["unit"] in self._supported_units):
            _unit = kwargs["unit"] if "unit" in kwargs else "None"
            raise ValueError(
                f"You must provide unit when defining {self}. This unit must be one of those types : {self._supported_units}. You provided {_unit}"
            )
        super().__init__(*args, **kwargs)
