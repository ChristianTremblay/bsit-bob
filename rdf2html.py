import os
import re

import click
import pyvis
from rdflib import Graph

g = Graph()
nodes = {}


def parse_rdf(ttl_file):
    global g
    with open(ttl_file, "r") as ttl:
        lines = ttl.read()
    graph = g.parse(data=lines, format="turtle")
    return graph


class Node:
    groups = {
        "Equipment": {
            "size": 20,
            "color": "green",
            "shape": "square",
            "group_int": 1,
            "borderWidth": None,
            "uri": "bob:legend/Equipment",
            "label": "Legend / Equipment",
        },
        "Connection": {
            "size": 15,
            "color": "purple",
            "shape": "diamond",
            "group_int": 2,
            "borderWidth": None,
            "uri": "bob:legend/Connection",
            "label": "Legend / Connection",
        },
        "InletConnectionPoint": {
            "size": 15,
            "color": "purple",
            "shape": "triangle",
            "group_int": 3,
            "borderWidth": None,
            "uri": "bob:legend/InletConnectionPoint",
            "label": "Legend / InletConnectionPoint",
        },
        "OutletConnectionPoint": {
            "size": 15,
            "color": "#9be0b6",
            "shape": "triangleDown",
            "group_int": 4,
            "borderWidth": None,
            "uri": "bob:legend/OutletConnectionPoint",
            "label": "Legend / OutletConnectionPoint",
        },
        "FunctionBlock": {
            "size": 15,
            "color": "#9be0b6",
            "shape": "star",
            "group_int": 4,
            "borderWidth": None,
            "uri": "bob:legend/FunctionBlock",
            "label": "Legend / FunctionBlock|Producer",
        },
        "DomainSpace": {
            "size": 15,
            "color": "#9be0b6",
            "shape": "box",
            "group_int": 4,
            "borderWidth": 2,
            "uri": "bob:legend/DomainSpace",
            "label": "Legend / DomainSpace",
        },
        "qudt": {
            "size": 10,
            "color": "#e3a1dd",
            "shape": "star",
            "group_int": 5,
            "borderWidth": None,
            "uri": "bob:legend/qudt",
            "label": "Legend / qudt",
        },
        "Default": {
            "size": 15,
            "color": None,
            "shape": "dot",
            "group_int": 0,
            "borderWidth": None,
            "uri": "bob:legend/Default",
            "label": "Legend / Default",
        },
    }

    def __init__(self, s, p=None, o=None):
        self.ns = set()
        self.types = set()
        self.aspects = set()
        self.uri = None
        self.label = None
        self.comment = None
        self.value = None
        self.medium = set()
        self.uri = str(s)
        self.quantityKind = set()
        self.enumerationKind = set()
        self.domain = set()
        self.unit = set()
        self.bacnet = {}

        if p and o:
            if "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" in p:
                self.ns.add(str(o))
            self.add_info(s, p, o)
            if "label" not in p and "comment" not in p:
                self.namespace_and_type(o)
        else:
            self.namespace_and_type(s)

    def namespace_and_type(self, info):
        if "urn" in info:
            return
        try:
            ns, _type = prefix(info)
            self.ns.add(ns)
            self.types.add(_type)
        except TypeError:
            pass

    @property
    def group_name(self):
        if "s223:Equipment" in self.types:
            return "Equipment"
        elif "s223:Connection" in self.types:
            return "Connection"
        elif "s223" in self.types:
            return "s223"
        elif (
            "s223:InletConnectionPoint" in self.types
            or "s223:FunctionInput" in self.types
            or "p223:ProducerInput" in self.types
            or "s223:BidirectionalConnectionPoint" in self.types
        ):
            return "InletConnectionPoint"
        elif (
            "s223:OutletConnectionPoint" in self.types
            or "s223:FunctionOutput" in self.types
            or "p223:ProducerOutput" in self.types
        ):
            return "OutletConnectionPoint"
        elif "p223:Producer" in self.types or "s223:FunctionBlock" in self.types:
            return "FunctionBlock"
        elif "s223:DomainSpace" in self.types or "s223:PhysicalSpace" in self.types:
            return "DomainSpace"
        else:
            return "Default"

    @property
    def group(self):
        return self.groups[self.group_name]["group_int"]

    @property
    def size(self):
        return self.groups[self.group_name]["size"]

    @property
    def color(self):
        return self.groups[self.group_name]["color"]

    @property
    def shape(self):
        return self.groups[self.group_name]["shape"]

    @property
    def borderWidth(self):
        return self.groups[self.group_name]["borderWidth"]

    @property
    def title(self):
        _n = ", ".join(self.ns)
        _t = ", ".join(self.types)
        _bubble = f"Namespaces : {_n}\nTypes: {_t}"
        if self.comment:
            _bubble += f"\nComment : {self.comment}"
        if self.value:
            _bubble += f"\nValue : {self.value}"
        if self.aspects:
            _a = ", ".join(self.aspects)
            _bubble += f"\nAspects : {_a}"
        if self.medium:
            _m = ", ".join(self.medium)
            _bubble += f"\nMedium : {_m}"
        if self.quantityKind:
            _q = ", ".join(self.quantityKind)
            _bubble += f"\nQuantityKind : {_q}"
        if self.enumerationKind:
            _k = ", ".join(self.enumerationKind)
            _bubble += f"\nEnumerationKind : {_k}"
        if self.domain:
            _d = ", ".join(self.domain)
            _bubble += f"\nDomain : {_d}"
        if self.unit:
            _u = ", ".join(self.unit)
            _bubble += f"\nUnit : {_u}"
        if self.bacnet:
            for k, v in self.bacnet.items():
                _bubble += f"\n{k} : {v}"

        return _bubble

    def add_info(self, s, p, o):
        if "label" in p:
            self.label = str(o)
        elif "comment" in p:
            self.comment = o
        elif "ns#type" in p:
            self.namespace_and_type(o)
        elif "hasValue" in p:
            self.value = str(o)
        elif "hasAspect" in p:
            self.aspects.add(prefix(str(o))[1])
        elif "hasMedium" in p or "ofSubstance" in p or "ofMedium" in p:
            self.medium.add(prefix(str(o))[1])
        elif "hasQuantityKind" in p:
            self.quantityKind.add(prefix(str(o))[1])
        elif "hasEnumerationKind" in p:
            self.enumerationKind.add(prefix(str(o))[1])
        elif "hasDomain" in p:
            self.domain.add(prefix(str(o))[1])
        elif "qudt/unit" in p or "vocab/unit" in p:
            self.unit.add(prefix(str(o))[1])
        elif "http://data.ashrae.org/bacnet/2020#objectInstance" in p:
            self.bacnet["objectinstance"] = str(o)
        elif "http://data.ashrae.org/bacnet/2020#objectType" in p:
            self.bacnet["object_type"] = str(o)
        elif "http://data.ashrae.org/bacnet/2020#objectName" in p:
            self.bacnet["object_name"] = str(o)
        elif "http://data.ashrae.org/bacnet/2020#description" in p:
            self.bacnet["description"] = str(o)
        elif "http://data.ashrae.org/bacnet/2020#address" in p:
            self.bacnet["address"] = str(o)
        elif "http://data.ashrae.org/bacnet/2020#deviceName" in p:
            self.bacnet["deviceName"] = str(o)
        elif "http://data.ashrae.org/bacnet/2020#deviceId" in p:
            self.bacnet["deviceId"] = str(o)
        elif "http://data.ashrae.org/bacnet/2020#vendorId" in p:
            self.bacnet["vendorId"] = str(o)
        elif "http://data.ashrae.org/bacnet/2020#networkNumber" in p:
            self.bacnet["networkNumber"] = str(o)


def prepare_nodes(g):
    global nodes
    for s, p, o in g:
        if s not in nodes.keys():
            # print(f"Adding {s}")
            nodes[s] = Node(s, p, o)
        else:
            # print(f"Modifying {s} -> {nodes[s].uri}")
            nodes[s].add_info(s, p, o)
        if (
            o not in nodes.keys()
            and "label" not in p
            and "comment" not in p
            and "ns#type" not in p
            and "hasValue" not in p
            and "hasAspect" not in p
            and "hasMedium" not in p
            and "hasQuantityKind" not in p
            and "ofMedium" not in p
            and "ofSubstance" not in p
            and "hasEnumerationKind" not in p
            and "hasDomain" not in p
            and "vocab/unit" not in p
            and "qudt/unit" not in p
            and "2020#objectInstance" not in p
            and "2020#objectType" not in p
            and "2020#objectName" not in p
            and "2020#description" not in p
            and "2020#address" not in p
            and "2020#deviceName" not in p
            and "2020#deviceId" not in p
            and "2020#vendorId" not in p
            and "2020#networkNumber" not in p
        ):
            nodes[o] = Node(o)


def make_legend(g):
    # Add Legend Nodes
    step = 100
    x = 2000
    y = -1000
    for k, v in Node.groups.items():
        g.add_node(
            v["uri"],
            group=v["group_int"],
            label=v["label"],
            size=v["size"],
            borderWidth=v["borderWidth"],
            # 'fixed': True, # So that we can move the legend nodes around to arrange them better
            physics=False,
            x=x,
            y=f"{y + v['group_int']*step}px",
            shape=v["shape"],
            widthConstraint=500,
            font={"size": 20},
        )


def prefix(full):
    _prefixes = [
        ("bob", "http://data.ashrae.org/standard223/si-builder#"),
        ("ex1", "urn:ex/sample_highLegDelta_electrical_entry/"),
        ("owl", "http://www.w3.org/2002/07/owl#"),
        ("p223", "http://data.ashrae.org/proposal-to-standard223#"),
        ("quantitykind", "http://qudt.org/vocab/quantitykind/"),
        ("qudt", "http://qudt.org/schema/qudt/"),
        ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
        ("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
        ("s223", "http://data.ashrae.org/standard223#"),
        ("unit", "http://qudt.org/vocab/unit/"),
        ("xsd", "http://www.w3.org/2001/XMLSchema#"),
        ("rec", "https://w3id.org/rec/core/"),
        ("bacnet", "http://data.ashrae.org/bacnet/2020#"),
        ("g36", "http://data.ashrae.org/standard223/1.0/extension/g36#"),
        ("ref", "https://brickschema.org/schema/Brick/ref#"),
        ("brick", "https://brickschema.org/schema/Brick#"),
    ]
    for each in _prefixes:
        _p, _f = each
        if _f in full:
            return (_p, full.replace(_f, f"{_p}:"))


def to_html(ttl_file, filter_urn=False, remove_basic_classes=False, show=False):
    global g, nodes
    g = parse_rdf(ttl_file)
    prepare_nodes(g)

    visual_graph = pyvis.network.Network(
        select_menu=True, filter_menu=True, cdn_resources="remote"
    )

    for k, v in nodes.items():
        # print(f"Adding to viz : {v.uri}")
        visual_graph.add_node(
            v.uri,
            v.label,
            title=v.title,
            size=v.size,
            color=v.color,
            shape=v.shape,
            group=v.group,
            borderWidth=v.borderWidth,
        )

    for s, p, o in g:
        try:
            visual_graph.add_edge(str(s), str(o), title=str(p))
        except AssertionError as error:
            # print(f"Problem adding edge to {s} | {p} | {o} : {error}")
            continue  # we don't want thoses nodes (aspects, medium, label, etc.)

    make_legend(visual_graph)

    visual_graph.toggle_physics(True)
    visual_graph.show_buttons()
    html_filename = f"{ttl_file.split('.ttl')[0]}.html"
    if show:
        visual_graph.show(html_filename, notebook=False)
    else:
        visual_graph.write_html(html_filename, notebook=False)
    visual_graph = None
    del visual_graph


def find_ttl_files(folder, found=[]):
    ttl_name_std = re.compile(r".ttl$")
    files_found = found
    for each in list(os.scandir(folder)):
        # print(each)
        if each.is_file():
            file = each.name
            # print('Name : ', file)
            if ttl_name_std.search(file):
                # print('Found : ', file)
                files_found.append(os.path.join(folder, file))
        elif each.is_dir() and each.name not in (".", ".git"):
            find_ttl_files(each, found=files_found)
    return files_found


def clear() -> None:
    """Remove all the triples from the graph, reset the blank node counter."""
    global g
    # remove all the triples
    g.remove((None, None, None))
    del g
    g = Graph()


@click.command()
@click.option("-v", "--view", default=False)
@click.argument("folder", type=click.Path(), required=False)
def convert_all(folder=None, file=None, view=False):
    if file:
        to_html(file, show=view)
    if folder:
        _convert_all(folder)


def _convert_all(folder):
    files = find_ttl_files(folder)
    for each in files:
        p = os.path.normpath(each)
        print(f"Processing {p}")
        to_html(p)
        clear()


@click.command()
@click.argument("file")
def process(folder=None, file=None, view=False):
    if file:
        to_html(file, show=view)


if __name__ == "__main__":
    process()
