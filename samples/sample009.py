import logging
from pathlib import Path

from header import sample_header

from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import (
    Equipment,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    System,
    bind_model_namespace,
    dump,
)

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class EquipmentIn1(Equipment):
    cp: AirInletConnectionPoint


class SystemIn1(System):
    cp: InletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        Equipment = EquipmentIn1(label=kwargs["label"] + "-d")
        self.cp.mapsTo = Equipment.cp


class EquipmentIn2(Equipment):
    cp1: AirInletConnectionPoint
    cp2: AirInletConnectionPoint


class SystemIn2(System):
    cp1: InletSystemConnectionPoint
    cp2: InletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        Equipment = EquipmentIn2(label=kwargs["label"] + "-d")
        self.cp1.mapsTo = Equipment.cp1
        self.cp2.mapsTo = Equipment.cp2


class EquipmentOut1(Equipment):
    cp: AirOutletConnectionPoint


class SystemOut1(System):
    cp: OutletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        Equipment = EquipmentOut1(label=kwargs["label"] + "-d")
        self.cp.mapsTo = Equipment.cp


class EquipmentOut2(Equipment):
    cp1: AirOutletConnectionPoint
    cp2: AirOutletConnectionPoint


class SystemOut2(System):
    cp1: OutletSystemConnectionPoint
    cp2: OutletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        Equipment = EquipmentOut2(label=kwargs["label"] + "-d")
        self.cp1.mapsTo = Equipment.cp1
        self.cp2.mapsTo = Equipment.cp2


class EquipmentInOut(Equipment):
    cp1: AirInletConnectionPoint
    cp2: AirOutletConnectionPoint


class SystemInOut(System):
    cp1: InletSystemConnectionPoint
    cp2: OutletSystemConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        Equipment = EquipmentInOut(label=kwargs["label"] + "-d")
        self.cp1.mapsTo = Equipment.cp1
        self.cp2.mapsTo = Equipment.cp2


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
dump(filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name))
