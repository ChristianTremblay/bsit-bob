from pathlib import Path

import logging
from bob.core import (
    bind_model_namespace,
    System,
    SystemInletConnectionPoint,
    SystemOutletConnectionPoint,
    dump,
    clear,
)

from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class SystemIn1(System):
    cp: SystemInletConnectionPoint


class SystemIn2(System):
    cp1: SystemInletConnectionPoint
    cp2: SystemInletConnectionPoint


class SystemOut1(System):
    cp: SystemOutletConnectionPoint


class SystemOut2(System):
    cp1: SystemOutletConnectionPoint
    cp2: SystemOutletConnectionPoint


class SystemInOut(System):
    cp1: SystemInletConnectionPoint
    cp2: SystemOutletConnectionPoint


# two independant systems
s1 = SystemIn1(label="s1")
s2 = SystemOut1(label="s2")

# s1 is connected to s2 (wrong direction) via connection points
s1 = SystemIn1(label="s1")
s2 = SystemOut1(label="s2")

try:
    s1.cp >> s2.cp
    raise AssertionError("failed to raise runtime error")
except TypeError as err:
    logging.info(f"caught: {err}\n")

# s1 is connected from s2 (correct direction) via connection points
s1 = SystemIn1(label="s1")
s2 = SystemOut1(label="s2")

s2.cp >> s1.cp

# s1 is connected to s2 (wrong direction)
s1 = SystemIn1(label="s1")
s2 = SystemOut1(label="s2")

try:
    s1 >> s2
    raise AssertionError("failed to raise runtime error")
except RuntimeError as err:
    logging.info(f"caught: {err}\n")

# s1 is connected from s2 (correct direction)
s1 = SystemIn1(label="s1")
s2 = SystemOut1(label="s2")

s2 >> s1

# s2 is connected to s1 (ambiguous destinations)
s1 = SystemIn2(label="s1")
s2 = SystemOut1(label="s2")

try:
    s2 >> s1
    raise AssertionError("failed to raise runtime error")
except RuntimeError as err:
    logging.info(f"caught: {err}\n")

# s2 is connected to s1 (ambiguous sources)
s1 = SystemIn1(label="s1")
s2 = SystemOut2(label="s2")

try:
    s2 >> s1
    raise AssertionError("failed to raise runtime error")
except RuntimeError as err:
    logging.info(f"caught: {err}\n")

# s1 >> s2 >> s3
s1 = SystemOut1(label="s1")
s2 = SystemInOut(label="s2")
s3 = SystemIn1(label="s3")

s1 >> s2 >> s3

# s3 << s2 << s1
s1 = SystemOut1(label="s1")
s2 = SystemInOut(label="s2")
s3 = SystemIn1(label="s3")

s3 << s2 << s1

# dump the result
sample_header(model_name)
dump()
