from bob.core import bind_model_namespace, System, Device, Connection, Inlet, Outlet, dump, clear

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class DeviceIn(Device):
    cpIn: Inlet


class DeviceInOut(Device):
    cpIn: Inlet
    cpOut: Outlet


class DeviceOut(Device):
    cpOut: Outlet


class SystemInOut(System):
    cpIn1: Inlet
    cpIn2: Inlet
    cpOut1: Outlet
    cpOut2: Outlet


d1 = DeviceInOut(label="D1")
d2 = DeviceInOut(label="D2")
d3 = DeviceInOut(label="D3")
d4 = DeviceInOut(label="D4")
d5 = DeviceInOut(label="D5")
d6 = DeviceIn(label="D6")
d7 = DeviceOut(label="D7")
d8 = DeviceInOut(label="D8")
d9 = DeviceInOut(label="D9")

c1 = Connection(label="C1")
c2 = Connection(label="C2")
c3 = Connection(label="C3")
c4 = Connection(label="C4")
c5 = Connection(label="C5")
c6 = Connection(label="C6")
c7 = Connection(label="C7")
c8 = Connection(label="C8")
c9 = Connection(label="C9")

s1 = SystemInOut(label="S1")

# D5, D8, and D9 are devices inside S1
d5 < s1
d8 < s1
d9 < s1

# simple connections
d1 >> c1 >> d2
d2 >> c2 >> d3
c2 >> d4

# half-connections outside the system
d4 >> c3
c6 >> d6
d7 >> c7

# connections inside the system
c4 >> d5 >> c5
c8 >> d8 >> c9
c8 >> d9 >> c9
c9 >> s1.cpOut2

# bridge through a system
c3 >> s1.cpIn1 >> c4
c5 >> s1.cpOut1 >> c6
c7 >> s1.cpIn2 >> c8

dump()

