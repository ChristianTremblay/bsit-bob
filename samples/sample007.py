from pathlib import Path

from bob import bind_model_namespace, Device, Part, dump, clear

from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TestDevice(Device):
    pass


class Part1(Part):
    pass


class Part2(Part):
    pass


# device has two parts
d = TestDevice(label="Test Device 1")
p1 = Part1()
p2 = Part2()

d > p1
d > p2

# device has a part p1 which has a part p2
d = TestDevice(label="Test Device 2")
p1 = Part1()
p2 = Part2()

d > p1 > p2

# p1 is a part of p2 which is a part of a device
d = TestDevice(label="Test Device 3")
p1 = Part1()
p2 = Part2()

p1 < p2 < d

# dump the result
sample_header(model_name)
dump()
