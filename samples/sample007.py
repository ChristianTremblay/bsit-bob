from bob import bind_model_namespace, Device, Part, dump, clear

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class TestDevice(Device):
    pass


class Part1(Part):
    pass


class Part2(Part):
    pass


print("----- device has two parts -----")
d = TestDevice(label="TestDevice")
p1 = Part1()
p2 = Part2()

d > p1
d > p2

dump()
clear()
print("")

print("----- device has a part p1 which has a part p2 -----")
d = TestDevice(label="TestDevice")
p1 = Part1()
p2 = Part2()

d > p1 > p2

dump()
clear()
print("")

print("----- p1 is a part of p2 which is a part of a device -----")
d = TestDevice(label="TestDevice")
p1 = Part1()
p2 = Part2()

p1 < p2 < d

dump()
clear()
print("")

print("----- device 2 is a subdevice of device 1 -----")
d1 = TestDevice(label="Test Device 1")
d2 = TestDevice(label="Test Device 2")

d1 > d2

dump()
clear()
print("")

print("----- device 1 is a subdevice of device 2 -----")
d1 = TestDevice(label="Test Device 1")
d2 = TestDevice(label="Test Device 2")

d1 < d2

dump()
clear()
print("")
