import logging
from pathlib import Path

from bob.core import bind_model_namespace, data_graph, schema_graph, dump
from bob.scratch.header import sample_header

from bob.core import (
    Equipment,
    BoundaryConnectionPoint,
    System,
)
from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint

model_name = Path(__file__).stem
_namespace = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class EquipmentIn1(Equipment):
    cp: AirInletConnectionPoint


class SystemIn1(System):
    cp: BoundaryConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        equipment = EquipmentIn1(label=kwargs["label"] + "-d")

        self > equipment
        self.cp = equipment.cp


class EquipmentIn2(Equipment):
    cp1: AirInletConnectionPoint
    cp2: AirInletConnectionPoint


class SystemIn2(System):
    cp1: BoundaryConnectionPoint
    cp2: BoundaryConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        equipment = EquipmentIn2(label=kwargs["label"] + "-d")

        self > equipment
        self.cp1 = equipment.cp1
        self.cp2 = equipment.cp2


class EquipmentOut1(Equipment):
    cp: AirOutletConnectionPoint


class SystemOut1(System):
    cp: BoundaryConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        equipment = EquipmentOut1(label=kwargs["label"] + "-d")

        self > equipment
        self.cp = equipment.cp


class EquipmentOut2(Equipment):
    cp1: AirOutletConnectionPoint
    cp2: AirOutletConnectionPoint


class SystemOut2(System):
    cp1: BoundaryConnectionPoint
    cp2: BoundaryConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        equipment = EquipmentOut2(label=kwargs["label"] + "-d")

        self > equipment
        self.cp1 = equipment.cp1
        self.cp2 = equipment.cp2


class EquipmentInOut(Equipment):
    cp1: AirInletConnectionPoint
    cp2: AirOutletConnectionPoint


class SystemInOut(System):
    cp1: BoundaryConnectionPoint
    cp2: BoundaryConnectionPoint

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        equipment = EquipmentInOut(label=kwargs["label"] + "-d")

        self > equipment
        self.cp1 = equipment.cp1
        self.cp2 = equipment.cp2


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
dump(
    data_graph,
    filename=f"samples/ttl/{model_name}.data.ttl",
    header=sample_header(model_name),
)
dump(schema_graph, filename=f"samples/ttl/{model_name}.schema.ttl")
