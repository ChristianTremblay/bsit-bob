from bob.core import bind_model_namespace, System, Inlet, Outlet, dump, clear

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class SystemIn1(System):
    cp: Inlet


class SystemIn2(System):
    cp1: Inlet
    cp2: Inlet


class SystemOut1(System):
    cp: Outlet


class SystemOut2(System):
    cp1: Outlet
    cp2: Outlet


class SystemInOut(System):
    cp1: Inlet
    cp2: Outlet


print("----- two independant systems -----")
s1 = SystemIn1(label="s1")
s2 = SystemOut1(label="s2")

dump()
clear()
print("")

print("----- s1 is connected to s2 (wrong direction) via connection points -----")
s1 = SystemIn1(label="s1")
s2 = SystemOut1(label="s2")

try:
    s1.cp >> s2.cp
except RuntimeError as err:
    print(f"caught: {err}")

clear()
print("")

print("----- s1 is connected from s2 (correct direction) via connection points -----")
s1 = SystemIn1(label="s1")
s2 = SystemOut1(label="s2")

try:
    s2.cp >> s1.cp
except RuntimeError as err:
    print(f"caught: {err}")

dump()
clear()
print("")

print("----- s1 is connected to s2 (wrong direction) -----")
s1 = SystemIn1(label="s1")
s2 = SystemOut1(label="s2")

try:
    s1 >> s2
except RuntimeError as err:
    print(f"caught: {err}")

clear()
print("")

print("----- s1 is connected from s2 (correct direction) -----")
s1 = SystemIn1(label="s1")
s2 = SystemOut1(label="s2")

try:
    s2 >> s1
except RuntimeError as err:
    print(f"caught: {err}")

dump()
clear()
print("")

print("----- s2 is connected to s1 (ambiguous destinations) -----")
s1 = SystemIn2(label="s1")
s2 = SystemOut1(label="s2")

try:
    s2 >> s1
except RuntimeError as err:
    print(f"caught: {err}")

clear()
print("")

print("----- s2 is connected to s1 (ambiguous sources) -----")
s1 = SystemIn1(label="s1")
s2 = SystemOut2(label="s2")

try:
    s2 >> s1
except RuntimeError as err:
    print(f"caught: {err}")

clear()
print("")

print("----- s1 >> s2 >> s3 -----")
s1 = SystemOut1(label="s1")
s2 = SystemInOut(label="s2")
s3 = SystemIn1(label="s3")

s1 >> s2 >> s3

dump()
clear()
print("")

print("----- s3 << s2 << s1 -----")
s1 = SystemOut1(label="s1")
s2 = SystemInOut(label="s2")
s3 = SystemIn1(label="s3")

s3 << s2 << s1

dump()
clear()
print("")
