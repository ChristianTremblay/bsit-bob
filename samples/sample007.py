from bob import bind_model_namespace, Device, Part, dump, clear

from samples import sample_header


__namespace__ = bind_model_namespace("ex", "urn:ex/")


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

# device 5 is a subdevice of device 4
d4 = TestDevice(label="Test Device 4")
d5 = TestDevice(label="Test Device 5")

d4 > d5

# device 7 is a subdevice of device 6
d6 = TestDevice(label="Test Device 6")
d7 = TestDevice(label="Test Device 7")

d7 < d6

# dump the result
sample_header("sample007")
dump()
