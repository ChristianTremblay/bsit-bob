from bob.core import (
    Connection,
    Equipment,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    Junction,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    System,
    bind_model_namespace,
    clear,
    dump,
)

_namespace = bind_model_namespace("ex", "urn:ex/")


class EquipmentIn(Equipment):
    cpIn: InletConnectionPoint


class EquipmentInOut(Equipment):
    cpIn: InletConnectionPoint
    cpOut: OutletConnectionPoint


class EquipmentOut(Equipment):
    cpOut: OutletConnectionPoint


class SystemInOut(System):
    cpIn1: InletSystemConnectionPoint
    cpIn2: InletSystemConnectionPoint
    cpOut1: OutletSystemConnectionPoint
    cpOut2: OutletSystemConnectionPoint


d1 = EquipmentInOut(label="D1")
d2 = EquipmentInOut(label="D2")
d3 = EquipmentInOut(label="D3")
d4 = EquipmentInOut(label="D4")
d5 = EquipmentInOut(label="D5")
d6 = EquipmentIn(label="D6")
d7 = EquipmentOut(label="D7")
d8 = EquipmentInOut(label="D8")
d9 = EquipmentInOut(label="D9")

c1 = Connection(label="C1")
c2 = Connection(label="C2")

s1 = SystemInOut(label="S1")

# D5, D8, and D9 are Equipments inside S1
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

# Equipment to system connections
d4 >> s1.cpIn1
s1.cpOut1 >> d6
d7 >> s1.cpIn2

dump()
