from pathlib import Path

import logging
from bob.core import (
    bind_model_namespace,
    Device,
    InletConnectionPoint,
    OutletConnectionPoint,
    System,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    dump,
)

from header import sample_header


model_name = Path(__file__).stem
__namespace__ = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class DeviceIn1(Device):
    cp: InletConnectionPoint


class SystemIn1(System):
    cp: InletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        device = DeviceIn1(label=kwargs["label"] + "-d")
        self.cp.mapsTo = device.cp


class DeviceIn2(Device):
    cp1: InletConnectionPoint
    cp2: InletConnectionPoint


class SystemIn2(System):
    cp1: InletSystemConnectionPoint
    cp2: InletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        device = DeviceIn2(label=kwargs["label"] + "-d")
        self.cp1.mapsTo = device.cp1
        self.cp2.mapsTo = device.cp2


class DeviceOut1(Device):
    cp: OutletConnectionPoint


class SystemOut1(System):
    cp: OutletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        device = DeviceOut1(label=kwargs["label"] + "-d")
        self.cp.mapsTo = device.cp


class DeviceOut2(Device):
    cp1: OutletConnectionPoint
    cp2: OutletConnectionPoint


class SystemOut2(System):
    cp1: OutletSystemConnectionPoint
    cp2: OutletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        device = DeviceOut2(label=kwargs["label"] + "-d")
        self.cp1.mapsTo = device.cp1
        self.cp2.mapsTo = device.cp2


class DeviceInOut(Device):
    cp1: InletConnectionPoint
    cp2: OutletConnectionPoint


class SystemInOut(System):
    cp1: InletSystemConnectionPoint
    cp2: OutletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        device = DeviceInOut(label=kwargs["label"] + "-d")
        self.cp1.mapsTo = device.cp1
        self.cp2.mapsTo = device.cp2


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

# dump the result
dump(filename=f"ttl/{model_name}.ttl", header=sample_header(model_name))
