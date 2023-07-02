from rdflib import Graph

g = Graph()
nodes = {}


def parse_rdf(ttl_file):
    global g
    with open(ttl_file, "r") as ttl:
        lines = ttl.read()
    graph = g.parse(data=lines, format="turtle")
    return graph


g = parse_rdf("VOCAB_SP223_electricity-v1.0.ttl")

title = None
details = None
class_name = None
medium = None

header = """
from rdflib import Literal, URIRef

from ..core import (
    BOB,
    S223,
    Connection,
    ConnectionPoint,
    Electricity,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    SystemConnectionPoint,
)

_namespace = S223

# === Generic
# Undefined Electrical


class ElectricalConnection(Connection):
    hasMedium = Electricity
    _class_iri = S223.Connection


class ElectricalConnectionPoint(ConnectionPoint):
    hasMedium = Electricity


class ElectricalInletConnectionPoint(
    InletConnectionPoint, ElectricalConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class ElectricalOutletConnectionPoint(
    OutletConnectionPoint, ElectricalConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class ElectricalSystemConnectionPoint(SystemConnectionPoint):
    hasMedium = Electricity


class ElectricalSystemInletConnectionPoint(
    ElectricalSystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class ElectricalSystemOutletConnectionPoint(
    ElectricalSystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint

"""


# title, details, class name, medium

lst = set()
for s, p, o in g:
    try:
        if ("Electricity-AC" in o or "Electricity-DC" in o) and "ns#type" in p:
            print(s, p, o)
            _title = s.split("#")[1]
            if "Electricity-AC" in o:
                _details = "3 Phases" if "3Ph" in _title else "1 phase"
                _class_name = _title.split("AC-")[1].replace("-", "_").replace(".", "r")
                _medium_suffix = _title.split("AC-")[1]
                _ACDC = "AC"
            else:
                _details = "DC"
                _class_name = _title.split("DC-")[1].replace("-", "_").replace(".", "r")
                _medium_suffix = _title.split("DC-")[1]
                _ACDC = "DC"

            cn = f"Electricity_{_class_name}"
            _medium = f"Electricity.{_ACDC}{_class_name}"
            # print(title, details, class_name, medium)
            lst.add((_title, _details, cn, _medium, _medium_suffix, _ACDC))
    except Exception as error:
        print(s, p, o)

print(lst)
print(f"There are {len(lst)} elements")
with open("new_electricity.py", "w") as file:
    file.write(header)

    for each in sorted(lst):
        title, details, class_name, medium, _, _ = each
        for element in [
            ("{title}", title),
            ("{details}", details),
            ("{class_name}", class_name),
            ("{medium}", medium),
        ]:
            template = f"""
# === {title}
# {details}


class {class_name}Connection(Connection):
    hasMedium = {medium}
    _class_iri = S223.Connection


class {class_name}ConnectionPoint(ConnectionPoint):
    hasMedium = {medium}


class {class_name}InletConnectionPoint(
    InletConnectionPoint, {class_name}ConnectionPoint
):
    _class_iri = S223.InletConnectionPoint


class {class_name}OutletConnectionPoint(
    OutletConnectionPoint, {class_name}ConnectionPoint
):
    _class_iri = S223.OutletConnectionPoint


class {class_name}SystemConnectionPoint(SystemConnectionPoint):
    hasMedium = {medium}


class {class_name}SystemInletConnectionPoint(
    {class_name}SystemConnectionPoint, InletSystemConnectionPoint
):
    _class_iri = BOB.InletSystemConnectionPoint


class {class_name}SystemOutletConnectionPoint(
    {class_name}SystemConnectionPoint, OutletSystemConnectionPoint
):
    _class_iri = BOB.OutletSystemConnectionPoint"""

            _t, _n = element
            template = template.replace(_t, _n)
        file.write(template)
with open("add_to_media.py", "w") as file:
    for each in sorted(lst):
        title, details, class_name, medium, suffix, _ACDC = each
        for element in [
            ("{medium}", medium),
            ("{suffix}", suffix),
        ]:
            template = f"""
{medium} = Electricity.{_ACDC}("{suffix}")"""
            _t, _n = element
            template = template.replace(_t, _n)
        file.write(template)
