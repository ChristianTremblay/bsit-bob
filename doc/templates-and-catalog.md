# Templates and Catalog

Catalog source
- Use `catalog_source: si_templates|get_template` to load catalog items.
- `from_catalog` pulls reusable blocks (sensors, controllers, packages).

Example: Using from_catalog for sensors
```yaml
from_catalog:
  STG:
    template: generic.sensor.rtd
    hasUnit: UNIT.DEG_C
  TPD:
    template: differential_pressure
    hasUnit: UNIT.PA
```

Programmatic instantiation
```python
from bob.template import config_from_yaml
from scratch.schemaorg import ProductGroupFromTemplate

config = config_from_yaml("ahu.yaml")
ahu = ProductGroupFromTemplate(config=config, label="SYSTEM_1")
```

When to create custom templates
- Missing CPs (e.g., VFD modulation/status).
- Multi-sensor “equipment” with IO CPs (RTD, 0-10V, 4-20mA).
- Assemblies (e.g., Humidifier with controller and auxiliaries).

Expose CPs via controller_mapsTo only if external layer needs them.

See also
- [Sensors and Observation Locations](sensors-and-observation.md)
