"""
Build Dizzy

Application that sucks in the Brick.ttl file and spits out a Bob module.
"""
import sys

from collections import defaultdict
from copy import deepcopy
from textwrap import fill, indent
from typing import Dict, List, Set

from rdflib import RDF, RDFS, SKOS, Graph, Namespace, URIRef

BOB = Namespace("http://data.ashrae.org/standard223/si-builder#")
REC = Namespace("https://w3id.org/rec#")

triple_quote = '"""\n'

# globals
subclass_map: Dict[URIRef, Set[URIRef]] = {}
superclass_map: Dict[URIRef, Set[URIRef]] = {}

# special things
rec_alignment = {
    REC.Space: ["_PhysicalSpace"],
    REC.Information: ["_Node"],
    REC.Collection: ["_Node"],
    REC.BuildingElement: ["_Node"],
    REC.Event: ["_Node"],
    REC.Asset: ["_Node"],
    REC.Agent: ["_Node"],
}


def register_dependency(cls, subcls):
    """
    Note the fact that class `cls` depends on one of its subclasses `subcls`.
    """
    global subclass_map

    if cls not in subclass_map:
        subclass_map[cls] = set()
    if subcls not in subclass_map:
        subclass_map[subcls] = set()

    subclass_map[cls].add(subcls)

    if subcls not in superclass_map:
        superclass_map[subcls] = set()
    if cls not in superclass_map:
        superclass_map[cls] = set()

    superclass_map[subcls].add(cls)


def topological_sort() -> List[str]:
    """
    Perform topological sort on the subclass dependancies.
    """
    global subclass_map

    result: List[URIRef] = []

    pending = list(deepcopy(subclass_map).items())
    emitted: List[URIRef] = []
    while pending:
        next_pending = []
        next_emitted = []
        for entry in pending:
            element, deps = entry
            deps.difference_update(set((element,)), emitted)
            if deps:
                next_pending.append(entry)
            else:
                result.append(element)
                emitted.append(element)
                next_emitted.append(element)
        if not next_emitted:
            raise ValueError(f"cyclic dependancy detected: {element}")
        pending = next_pending
        emitted = next_emitted

    return result


def cname(uri):
    """
    Return the simplified version of the URI.
    """
    return str(uri).split("#")[-1].replace(".", "_")


#
#   __main__
#

g = Graph()
g.parse(sys.argv[1], format="turtle")

for s, _, o in g.triples((None, RDFS.subClassOf, None)):
    if (s not in REC) or (o not in REC):
        continue
    register_dependency(s, o)

# sort the dependancies
sorted_deps = topological_sort()
seen = set()


def dump(elem):
    if elem in seen:
        return

    class_name = cname(elem)

    # build a list of dependancies sorted in the order that they are already
    # defined in the module
    class_deps = list(sorted(subclass_map[elem], key=lambda x: -sorted_deps.index(x)))
    if elem in rec_alignment:
        class_deps.extend(rec_alignment[elem])
    dep_names = ", ".join(cname(y) for y in class_deps)

    print("")
    print(f"class {class_name}({dep_names}):")

    # maybe some documentation
    definition = None
    if (elem, SKOS.definition, None) in g:
        definition = g.value(elem, SKOS.definition)
    elif (elem, RDFS.comment, None) in g:
        definition = g.value(elem, RDFS.comment)
    if definition:
        definition_text = indent(
            triple_quote + fill(definition) + "\n" + triple_quote, "    "
        )
        print(definition_text)

    # class name might have special characters in it
    if elem != REC[class_name]:
        cls_iri = str(elem).split("#")[-1]
        print(f'    _class_iri: URIRef = REC["{cls_iri}"]')

    print("    pass")

    seen.add(elem)

    if elem in superclass_map:
        children = sorted(superclass_map[elem])
        for child in children:
            parents_seen = all(parent in seen for parent in subclass_map[child])
            if parents_seen:
                dump(child)


print(
    '''
"""
Lofty - Real Estate Core Schema Classes for Bob
"""

from rdflib import URIRef
from bob.core import (
    bind_namespace,
    Node as _Node,
    Equipment as _Equipment,
    PhysicalSpace as _PhysicalSpace
)
from bob.equipment.hvac.fan import Fan as _Fan

_namespace = REC = bind_namespace("rec", "https://w3id.org/rec#")

'''
)

for k in subclass_map:
    if not subclass_map[k]:
        dump(k)
