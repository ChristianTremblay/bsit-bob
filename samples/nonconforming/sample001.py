from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import (
    QUANTITYKIND,
    QUDT,
    UNIT,
    Equipment,
    QuantifiableObservableProperty,
    QuantifiableProperty,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)
from bob.scratch.header import sample_header

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

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
