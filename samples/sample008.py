import logging
from bob.core import bind_model_namespace, System, ConnectionPoint, dump, clear

from samples import sample_header

__namespace__ = bind_model_namespace("ex", "urn:ex/")


class TestSystem(System):
    cp: ConnectionPoint


# two independant systems
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

# s1 is a subsystem of s2
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

s1 < s2

# s1 is a supersystem of s2
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

s1 > s2

# s1 is connected to s2
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

s1.cp >> s2.cp

# s1 is connected from s2
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

s1.cp << s2.cp

# s1 is connected to s2, ambiguous
s1 = TestSystem(label="s1")
s2 = TestSystem(label="s2")

try:
    s1 >> s2
    raise AssertionError("failed to raise runtime error")
except RuntimeError as err:
    logging.info(f"caught: {err}\n")

# dump the result
sample_header("sample008")
dump()
