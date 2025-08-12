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
```

Equivalent Python
```{literalinclude} examples/fan_device.py
:language: python
```

![Rendered graph](_static/artifacts/basics_fan.svg)

---

## System (simple AHU fragment)

YAML template
```{literalinclude} examples/ahu_system.yaml
:language: yaml
```

Equivalent Python
```{literalinclude} examples/ahu_system.py
:language: python
```

![Rendered graph](_static/artifacts/basics_ahu.svg)
