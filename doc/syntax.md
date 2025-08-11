# YAML Syntax Reference

Top-level keys
- name: Template identifier
- template_class: System | Equipment | Controller | Space | Junction …
- params: Free-form metadata (label, comment, etc.)
- properties: Property nodes (class, unit)
- sensors: Sensor nodes (if modeled directly)
- cp: Connection points (typed inlets/outlets)
- equipment: Child equipment defined in-line
- physical_spaces: Ducts, rooms, plenums, zones…
- from_catalog: Reusable parts (optional; core docs avoid external catalogs)
- junctions: Multi-port nodes
- boundaries: Boundary CPs (also via operator Node|cp)
- <domain>_connections: air/electrical/water/steam/signal/controllers
- sensors_observation_location: Map sensors to connectables
- internal_references / external_references: Property mappings (also via @)

Abridged template (System)
```yaml
name: ahu_template
template_class: System
params:
  label: "SYSTEM 1"

equipment:
  SF:
    class: Fan
    cp:
      airInlet: AirInletConnectionPoint
      airOutlet: AirOutletConnectionPoint

junctions:
  MixedAirDuct:
    class: Junction
    hasMedium: Fluid.Air
    fromReturnAir: AirInletConnectionPoint
    fromOutdoorAir: AirInletConnectionPoint
    toFilter: AirOutletConnectionPoint

air_connections:
  - OADPR.damper.airOutlet >> MixedAirDuct.fromOutdoorAir
```

Controllers (IO only; BACnet profile kept separate)
```yaml
name: M1
template_class: [Controller]
cp:
  electricalInlet: Electricity_24VLN_1Ph_60HzInletConnectionPoint
  bacnet_mstp: RS485BidirectionalConnectionPoint
  in10: ModulationSignalInletConnectionPoint
  out7: ModulationSignalOutletConnectionPoint
```

See also
- [Templates and Catalog](templates-and-catalog.md)
- [Connections](connections.md)
