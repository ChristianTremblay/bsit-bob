from pathlib import Path

from bob.core import bind_model_namespace, data_graph, schema_graph, dump
from header import sample_header

from bob.core import QUANTITYKIND, QUDT, UNIT, Equipment, bind_model_namespace, dump
from bob.property import QuantifiableObservableProperty, QuantifiableProperty

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TemperatureProperty(QuantifiableProperty):
    hasQuantityKind = QUANTITYKIND.Temperature


class SampleEquipment(Equipment):
    pass


class SampleEquipment2(Equipment):
    hasTemp: QuantifiableObservableProperty


# test Equipment has attribute, hasTemp which is of type temperature property.

# individual pieces
d1 = SampleEquipment(label="Test Equipment 1")
temp = TemperatureProperty(75.5, hasUnit=UNIT.DEG_F, label="temp")

d1.add_property(temp)

# auto build value
d2 = SampleEquipment(label="Test Equipment 2")
d2.add_property(TemperatureProperty(90.5, hasUnit=UNIT.DEG_F, label="temp"))

# named property, kwarg value
d3 = SampleEquipment2(label="Test Equipment 3", hasTemp=100.5)

# needs a unit to validate
d3.hasTemp.hasQuantityKind = QUANTITYKIND.Temperature
d3.hasTemp.hasUnit = UNIT.DEG_F

# dump the result
dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name),
)
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl")
