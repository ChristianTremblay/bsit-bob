# Basics: Equipment, Systems, Spaces
> Definitions for Equipment, System, PhysicalSpace, DomainSpace, Zone, and Junction are drawn from the ASHRAE 223P RDF. See the Glossary page for the canonical descriptions.

This section mirrors the simplest patterns covered by tests and builds up progressively.

223P mapping (nodes and edges)
- Nodes are instances of s223:Concept subclasses:
  - Equipment → s223:Equipment
  - System → s223:System
  - Physical Space → s223:PhysicalSpace
  - Domain Space → s223:DomainSpace; Zone → s223:Zone
  - Junction → s223:Junction
- Edges are s223 relations:
  - Containment → s223:contains (Equipment, PhysicalSpace), s223:hasMember (System)
  - Connectivity → s223:hasConnectionPoint, s223:connectsAt/connectsThrough, s223:connectedTo/connectedFrom, s223:hasMedium
  - Location/Grouping → s223:hasPhysicalLocation, s223:encloses, s223:hasDomain, s223:hasZone

Equipment (single device)
```yaml
name: fan_device
template_class: Equipment
params: { label: "SF-1" }
cp:
  airInlet: AirInletConnectionPoint
  airOutlet: AirOutletConnectionPoint
```

System (group equipment at the same level)
```yaml
name: simple_system
template_class: System
params: { label: "AHU-1" }

equipment:
  SF:
    class: Fan
    cp:
      airInlet: AirInletConnectionPoint
      airOutlet: AirOutletConnectionPoint

air_connections:
  - OutsideAirDuct.airOutlet >> SF.airInlet
  - SF.airOutlet >> SupplyAirDuct.airInlet
```

Physical spaces (topology context)
```yaml
name: spaces_example
template_class: System
params: { label: "Spaces" }

physical_spaces:
  ReturnAirDuct:
    class: Duct
  SupplyAirDuct:
    class: Duct
  OutsideAirDuct:
    class: Duct
```

Tips
- Keep connections at the same layer (System level) unless you expose CPs via mapsTo.
- Start with minimal CPs and add only what tests require.
