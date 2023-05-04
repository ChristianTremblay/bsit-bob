title = None
details = None
class_name = None
medium = None

header = """
from rdflib import Literal, URIRef

from bob.enum import AnalogSignalTypeEnum, BinarySignalTypeEnum, ProtocolEnum
from bob.properties.network import Mbit_per_seconds

from ..core import (
    BOB,
    P223,
    S223,
    BidirectionalConnectionPoint,
    BidirectionalSystemConnectionPoint,
    Connection,
    ConnectionPoint,
    Electricity,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    InletZoneConnectionPoint,
    Medium,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    OutletZoneConnectionPoint,
    SystemConnectionPoint,
    enum,
)

_namespace = BOB
"""


template = """
# === {title}
# {details}


class {class_name}Connection(Connection):
    hasMedium = Electricity.{medium}
    _class_iri = S223.Connection


class {class_name}ConnectionPoint(ConnectionPoint):
    hasMedium = Electricity.{medium}


class {class_name}InletConnectionPoint(
    InletConnectionPoint, {class_name}ConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class {class_name}OutletConnectionPoint(
    OutletConnectionPoint, {class_name}ConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class {class_name}SystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity.{medium}


class {class_name}SystemInletConnectionPoint(
    {class_name}SystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class {class_name}SystemOutletConnectionPoint(
    {class_name}SystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint"""

# title, details, class name, medium
lst = [
    ["575V_60Hz", "3 phases", "Electricity_575V_60Hz", "Electricity.AC575_60Hz"],
    [
        "575V_60Hz",
        "1 phases",
        "Electricity_575V_1Ph_60Hz",
        "Electricity.AC600V1Ph_60Hz",
    ],
]


def generate(title, details, class_name, medium):
    global template
    title = title
    details = details
    class_name = class_name
    medium = medium
    # print(template)
    return template


with open("new_electricity.py", "a") as file:
    file.write(header)

    for each in lst:
        title, details, class_name, medium = each
        for each in [
            ("{title}", title),
            ("{details}", details),
            ("{class_name}", class_name),
            ("{medium}", medium),
        ]:
            _t, _n = each
            template = template.replace(_t, _n)
        file.write(generate(title, details, class_name, medium))
