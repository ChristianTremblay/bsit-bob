from bob.core import bind_model_namespace, dump, turtle
from bob.core import Property
from bob.property import (
    ActuatableProperty,
    ObservableProperty,
    QuantifiableActuatableProperty,
    QuantifiableProperty,
)

__namespace__ = bind_model_namespace("ex", "urn:ex/")

p1 = Property(1)

p2 = ActuatableProperty(2)

p3 = ObservableProperty("green")

from bob.core import qudt

p4 = QuantifiableProperty(4.5, hasUnit=qudt.DEG_F)

#
#
#

p6 = ObservableProperty("green", label="color")

#
#
#


class TestProperty1(Property):
    pass


p7 = TestProperty1(7)

#
#
#


class TestProperty2(Property):
    label = "test 2"


p8 = TestProperty2(8)

result = turtle()
dump()


def test_result():
    print(result)
