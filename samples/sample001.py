from pathlib import Path

from bob import bind_model_namespace, Device, QuantifiableProperty, Value, dump
from bob.core import qudt, quantitykind

from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TemperatureValue(Value):
    hasUnits = qudt.DEG_F


class TemperatureProperty(QuantifiableProperty):
    _value_class: type = TemperatureValue
    hasQuantityKind = quantitykind.Temperature


class TestDevice(Device):
    pass


class TestDevice2(Device):
    hasTemp: TemperatureProperty


# test device has attribute, hastemp which is of type temperature property.

# individual pieces
d1 = TestDevice(label="Test Device 1")
value = Value(hasSimpleValue=75.5, hasUnits=qudt.DEG_F)
temp = TemperatureProperty(value, label="temp")

d1.add_property(temp)

# auto build value
d2 = TestDevice(label="Test Device 2")
d2.add_property(TemperatureProperty(90.5, label="temp"))

# named property, kwarg value
d3 = TestDevice2(label="Test Device 3", hasTemp=100.5)

# dump the result
sample_header(model_name)
dump()
