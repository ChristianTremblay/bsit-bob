from bob.core import (
    bind_model_namespace,
    Junction,
    Connection,
    Device,
    InletConnectionPoint,
    OutletConnectionPoint,
    System,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    dump,
    clear,
)

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class DeviceIn(Device):
    cpIn: InletConnectionPoint


class DeviceInOut(Device):
    cpIn: InletConnectionPoint
    cpOut: OutletConnectionPoint


class DeviceOut(Device):
    cpOut: OutletConnectionPoint


class SystemInOut(System):
    cpIn1: InletSystemConnectionPoint
    cpIn2: InletSystemConnectionPoint
    cpOut1: OutletSystemConnectionPoint
    cpOut2: OutletSystemConnectionPoint


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

s1 = SystemInOut(label="S1")

# D5, D8, and D9 are devices inside S1
d5 < s1
d8 < s1
d9 < s1

# map the system conncetion points
s1.cpIn1.mapsTo = d5.cpIn
s1.cpOut1.mapsTo = d5.cpOut

# someday maybe: s1.cpIn2 >> [d8, d9]

# make a junction on the inlet side
j1 = Junction()
j1 >> d8.cpIn
j1 >> d9.cpIn
s1.cpIn2.mapsTo = j1

# someday maybe: s1.cpOut2 >> [d8, d9]

# make a junction on the outlet side
j2 = Junction()
j2 >> d8.cpOut
j2 >> d9.cpOut
s1.cpOut2.mapsTo = j2

# simple connections
d1 >> c1 >> d2
d2 >> c2 >> d3
c2 >> d4

# device to system connections
d4 >> s1.cpIn1
s1.cpOut1 >> d6
d7 >> s1.cpIn2

dump()
