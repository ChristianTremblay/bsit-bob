# Basics: Equipment, Systems, Spaces
> Definitions for Equipment, System, PhysicalSpace, DomainSpace, Zone, and Junction are drawn from the ASHRAE 223P RDF and aligned with Real Estate Core (see lofty.py). See the Glossary page for canonical descriptions.

This section mirrors the simplest patterns covered by tests and builds up progressively.

223P mapping (nodes and edges)
- Nodes are instances of s223:Concept subclasses:
  - Equipment → s223:Equipment
  - Junction → s223:Junction
- Edges are s223 relations:
  - Containment → s223:contains (Equipment, PhysicalSpace), s223:hasMember (System)
  - Location/Grouping → s223:hasPhysicalLocation, s223:encloses, s223:hasDomain, s223:hasZone

---

## Equipment (single device)

YAML template
```{literalinclude} examples/fan_device.yaml
:language: yaml
:caption: Example: fan_device.yaml
```

Equivalent Python
```{literalinclude} examples/fan_device.py
:language: python
:caption: Example: fan_device.py
```

```{figure} _static/artifacts/basics_fan.svg
:alt: Fan example graph
:align: center

Figure: basics_fan graph
```

```{admonition} Legend (SVG)
- Boxes: Equipment, Systems, Spaces, and other nodes
- Circles: s223:Property
- Diamonds: s223:ConnectionPoint
- Edge labels: s223 predicates (contains, hasMember, hasProperty, connectsAt, mapsTo, …)
```

```{literalinclude} _artifacts/basics_fan.ttl
:language: turtle
:caption: Listing: basics_fan.ttl
```

```{admonition} Legend (TTL)
- Prefixes declare namespaces (S223, BOB, EX, …)
- Triples are subject predicate object . in Turtle syntax
- Predicates align with s223 relations (contains, hasMember, hasProperty, connectsAt, …)
- The SVG filters common predicates; the TTL shows the full model content
```

---

## System (simple AHU fragment)

YAML template
```{literalinclude} examples/ahu_system.yaml
:language: yaml
:caption: Example: ahu_system.yaml
```

Equivalent Python
```{literalinclude} examples/ahu_system.py
:language: python
:caption: Example: ahu_system.py
```

```{figure} _static/artifacts/basics_ahu.svg
:alt: AHU example graph
:align: center

Figure: basics_ahu graph
```

```{admonition} Legend (SVG)
- Boxes: Equipment, Systems, Spaces, and other nodes
- Circles: s223:Property
- Diamonds: s223:ConnectionPoint
- Edge labels: s223 predicates (contains, hasMember, hasProperty, connectsAt, mapsTo, …)
```

```{literalinclude} _artifacts/basics_ahu.ttl
:language: turtle
:caption: Listing: basics_ahu.ttl
```

```{admonition} Legend (TTL)
- Prefixes declare namespaces (S223, BOB, EX, …)
- Triples are subject predicate object . in Turtle syntax
- Predicates align with s223 relations (contains, hasMember, hasProperty, connectsAt, …)
- The SVG filters common predicates; the TTL shows the full
