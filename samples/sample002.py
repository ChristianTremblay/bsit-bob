from pathlib import Path

from datetime import datetime
from bob.core import bind_model_namespace, Node, Property, Value, dump

from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class Test(Node):
    pass


class Snork(Node):
    test: Test
    temp: Property


# node assignment
s = Snork()
t = Test()
s.test = t

# node assignment via kwargs
s = Snork(test=Test())

# setting a property value
p = Property()
v = Value()
v.hasValue = 1
p.hasValue = v

# auto build Value, init property value
p = Property(4)

# kwargs set property value
p = Property(hasValue=5)

# datetime value
datetime_value = Value(datetime(2021, 1, 1))

# value with a timestamp
timestamp_value = Value(hasSimpleValue=22.5, hasTimestamp=datetime(2021, 1, 1))

# dump the result
sample_header(model_name)
dump()
