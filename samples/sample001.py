from pathlib import Path

from bob.core import qudt, quantitykind, bind_model_namespace, Device, dump
from bob.property import QuantifiableObservableProperty
from bob.property import QuantifiableProperty
from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TemperatureProperty(QuantifiableProperty):
    hasQuantityKind = quantitykind.Temperature


class TestDevice(Device):
    pass


class TestDevice2(Device):
    hasTemp: QuantifiableObservableProperty


# test device has attribute, hasTemp which is of type temperature property.

# individual pieces
d1 = TestDevice(label="Test Device 1")
temp = TemperatureProperty(75.5, unit=qudt.DEG_F, label="temp")

d1.add_property(temp)

# auto build value
d2 = TestDevice(label="Test Device 2")
d2.add_property(TemperatureProperty(90.5, unit=qudt.DEG_F, label="temp"))

# named property, kwarg value
d3 = TestDevice2(label="Test Device 3", hasTemp=(100.5))

# dump the result
sample_header(model_name)
dump()
