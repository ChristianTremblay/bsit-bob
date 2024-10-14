from datetime import datetime
from pathlib import Path

from bob.assemblage import create_data_and_schema_ttl
from bob.core import (
    Node,
    Property,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)
from bob.scratch.header import sample_header

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

_folder = Path(__file__).parent
create_data_and_schema_ttl(model_name, _folder, header=sample_header(model_name))
