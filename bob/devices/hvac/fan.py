from rdflib import URIRef
from typing import Dict

from bob.property import QuantifiableObservableProperty
from ...connections.electricity import ElectricalInletConnectionPoint
from ...core import s223, Device, quantitykind, unit


from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...signal import AnalogIn, AnalogOut
from ...sensor import define_sensors
from ...devices import contains_devices_list

__namespace__ = s223

"""
fan_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "contains": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
}
"""

class RPM(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.AngularVelocity
    unit: URIRef = unit["REV-PER-MIN"]

class Amps(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.ElectricCurrent
    unit: URIRef = unit.A

class HP(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Power
    unit: URIRef = unit.HP

class ElectricPower(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.Power
    unit: URIRef = unit.KiloW

class PowerFactor(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.PowerFactor
    unit: URIRef = unit.UNITLESS

class Fan(Device):
    node_type: URIRef = s223.Fan
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    electricalInlet: ElectricalInletConnectionPoint  # can come from a VFD
    amps: Amps
    rpm: RPM
    hp: HP
    kw: ElectricPower
    powerFactor: PowerFactor

    def __init__(self, config: Dict = None, **kwargs):
        optional_properties = ["electricalInlet", "amps", "rpm", "hp", "powerFactor"]
        _properties = {}
        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        sensors = define_sensors(config)
        devices, device_kwargs = contains_devices_list(config, **kwargs)
        for each in optional_properties:
            _properties[each] = device_kwargs.pop(each) if each in device_kwargs else None

        super().__init__(**device_kwargs)
        for k,v in _properties.items():
            try:
                self.each = self.__annotations__[k](v)
            except AttributeError:
                self.each = self.__annotations__[k](self)
        for sensor in sensors:
            self > sensor
        for dev in devices:
            self > dev
