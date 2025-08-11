# Connections

223P concepts
- Connection node → s223:Connection (with s223:hasMedium)
- Connection points → s223:ConnectionPoint (typed as Inlet/Outlet/Bidirectional)
- Binding edges → s223:connectsAt (Connection→CP), s223:connectsThrough (CP→Connection)
- Topology edges → s223:connectedTo / s223:connectedFrom (Connectable→Connectable)
- Medium edge → s223:hasMedium (on Connection and CP)

Syntax
```yaml
air_connections:
  - A.component.airOutlet >> B.component.airInlet     # creates a Connection and binds CPs
electrical_connections:
  - Source.electricalOutlet >> Target.electricalInlet
signal_connections:
  - Controller.out7 >> Actuator.modulationSignal
```

Rules
- Outlet >> Inlet; CP types carry medium direction (s223:InletConnectionPoint, s223:OutletConnectionPoint).
- Connection and all CPs must share a compatible s223:Substance-Medium (or constituent mix).
- Prefer System-level links; use mapsTo only when exposing internal CPs.

Troubleshooting
- Medium mismatch → check CP classes and any Junction hasMedium.
- Missing CP → add the CP with the correct CP class.
