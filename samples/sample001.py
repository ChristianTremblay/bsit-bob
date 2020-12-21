from bob import bind_model_namespace, Device, QuantifiableProperty, Value, dump, clear
from bob.core import qudt, quantitykind

from samples import sample_header


__namespace__ = bind_model_namespace("ex", "urn:ex/")


class TemperatureValue(Value):
    hasUnits = qudt.DEG_F


class TemperatureProperty(QuantifiableProperty):
    _value_class: type = TemperatureValue
    hasQuantityKind = quantitykind.Temperature


class TestDevice(Device):
    pass


class TestDevice2(Device):
    hasTemp: TemperatureProperty


# individual pieces
d1 = TestDevice(label="Test Device 1")
value = Value(hasSimpleValue=75.5, hasUnits=qudt.DEG_F)
temp = TemperatureProperty(value)

d1.add_property(temp)

# auto build value
d2 = TestDevice(label="Test Device 2")
d2.add_property(TemperatureProperty(90.5))

# named property, kwarg value
d3 = TestDevice2(label="Test Device 3", hasTemp=100.5)

# dump the result
sample_header("sample001")
dump()
