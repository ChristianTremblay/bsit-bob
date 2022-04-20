from datetime import datetime
from pathlib import Path

from header import sample_header

from bob.core import Node, Property, bind_model_namespace, dump

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


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
p = Property(4)

# kwargs set property value
p = Property(hasValue=5)

# value with a timestamp
# timestamp_value = Property(hasValue=22.5, hasTimestamp=datetime(2021, 1, 1))

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
