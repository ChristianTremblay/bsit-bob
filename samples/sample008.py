from bob.core import bind_model_namespace, System, ConnectionPoint, dump, clear

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class TestSystem(System):
    cp: ConnectionPoint


print("----- two independant systems -----")
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

dump()
clear()
print("")

print("----- s1 is a subsystem of s2 -----")
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

s1 < s2

dump()
clear()
print("")

print("----- s1 is a supersystem of s2 -----")
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

s1 > s2

dump()
clear()
print("")

print("----- s1 is connected to s2 -----")
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

s1.cp >> s2.cp

dump()
clear()
print("")

print("----- s1 is connected from s2 -----")
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

s1.cp << s2.cp

dump()
clear()
print("")

print("----- s1 is connected to s2, ambiguous -----")
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

try:
    s1 >> s2
except RuntimeError as err:
    print(f"caught: {err}")

clear()
print("")
