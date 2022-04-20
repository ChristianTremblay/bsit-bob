from pathlib import Path

from header import sample_header

from bob.core import Device, bind_model_namespace, dump, quantitykind, qudt, unit
from bob.property import QuantifiableObservableProperty, QuantifiableProperty

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TemperatureProperty(QuantifiableProperty):
    hasQuantityKind = quantitykind.Temperature


class SampleDevice(Device):
    pass


class SampleDevice2(Device):
    hasTemp: QuantifiableObservableProperty


# test device has attribute, hasTemp which is of type temperature property.

# individual pieces
d1 = SampleDevice(label="Test Device 1")
temp = TemperatureProperty(75.5, unit=unit.DEG_F, label="temp")

d1.add_property(temp)

# auto build value
d2 = SampleDevice(label="Test Device 2")
d2.add_property(TemperatureProperty(90.5, unit=unit.DEG_F, label="temp"))

# named property, kwarg value
d3 = SampleDevice2(label="Test Device 3", hasTemp=100.5)

# needs a unit to validate
d3.hasTemp.unit = unit.DEG_F

# dump the result

dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
