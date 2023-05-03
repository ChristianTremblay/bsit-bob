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
    def size(self):
        if "s223:Equipment" in self.types:
            return 20
        elif "s223:Connection" in self.types:
            return 15
        elif "s223" in self.types:
            return 10
        elif "s223:InletConnectionPoint" in self.types:
            return 15
        elif "s223:OutletConnectionPoint" in self.types:
            return 15
        elif "unit" in self.ns:
            return 10
        else:
            return 15

    @property
    def group(self):
        return self.uri

    @property
    def color(self):
        if "unit" in self.ns:
            return "#e3a1dd"
        elif "s223:Equipment" in self.types:
            return "green"
        elif "s223:Connection" in self.types:
            return "purple"
        elif "s223:InletConnectionPoint" in self.types:
            return "#2e754a"
        elif "s223:OutletConnectionPoint" in self.types:
            return "#9be0b6"
        else:
            return None

    @property
    def shape(self):
        if "unit" in self.ns:
            return "star"
        elif "s223:Equipment" in self.types:
            return "square"
        elif "s223:Connection" in self.types:
            return "diamond"
        elif "s223:InletConnectionPoint" in self.types:
            return "triangle"
        elif "s223:OutletConnectionPoint" in self.types:
            return "triangleDown"
        else:
            return "dot"

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
            self.aspects.add(str(o))
        elif "hasMedium" in p or "ofSubstance" in p:
            self.medium.add(prefix(str(o))[1])


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
            and "ofSubstance" not in p
        ):
            nodes[o] = Node(o)


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
            v.uri, v.label, title=v.title, size=v.size, color=v.color, shape=v.shape
        )

    for s, p, o in g:
        try:
            visual_graph.add_edge(str(s), str(o), title=str(p))
        except AssertionError as error:
            # print(f"Problem adding edge to {s} | {p} | {o} : {error}")
            continue  # we don't want thoses nodes (aspects, medium, label, etc.)

    visual_graph.toggle_physics(True)
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
