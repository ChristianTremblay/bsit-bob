from pathlib import Path

from header import sample_header

from bob.core import Device, bind_model_namespace, dump

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestDevice(Device):
    pass


class Part1(Device):
    pass


class Part2(Device):
    pass


# device has two parts
d1 = TestDevice(label="Test Device 1")
p11 = Part1(label="p11")
p12 = Part2(label="p12")

d1 > p11
d1 > p12

# device has a part p1 which has a part p2
d2 = TestDevice(label="Test Device 2")
p21 = Part1(label="p21")
p22 = Part2(label="p22")

d2 > p21 > p22

# p1 is a part of p2 which is a part of a device
d3 = TestDevice(label="Test Device 3")
p31 = Part1(label="p31")
p32 = Part2(label="p32")

p31 < p32 < d3

# dump the result
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
