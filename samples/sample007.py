from bob import bind_model_namespace, Device, Part, dump, clear

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class TestDevice(Device):
    pass


class Part1(Part):
    pass


class Part2(Part):
    pass


# build from pieces
print("----- test 1 -----")
d = TestDevice(label="TestDevice")
p1 = Part1()
p2 = Part2()

d > p1
d > p2

dump()
clear()
print("")

# build from pieces
print("----- test 2 -----")
d = TestDevice(label="TestDevice")
p1 = Part1()
p2 = Part2()

d > p1 > p2

dump()
clear()
print("")

# build from pieces
print("----- test 3 -----")
d = TestDevice(label="TestDevice")
p1 = Part1()
p2 = Part2()

p1 < p2 < d

dump()
clear()
print("")

# build from pieces
print("----- test 4 -----")
d1 = TestDevice(label="Test Device 1")
d2 = TestDevice(label="Test Device 2")

d1 > d2  # subsystem relationship

dump()
clear()
print("")

# build from pieces
print("----- test 5 -----")
d1 = TestDevice(label="Test Device 1")
d2 = TestDevice(label="Test Device 2")

d1 < d2  # subsystem relationship

dump()
clear()
print("")
