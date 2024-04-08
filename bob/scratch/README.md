# Scratch

Scratch is providing opiniated templates that can be used as example or starting points to create your own vrsion of s223 equipment.

They rely on the template mechanism supported by Bob where a configuration dictionnary can be provided when creatig an instance of an equipment or a system.

The format of the template is the same for equipment or systems.

```python
template_for_a_system = {
    "equipment": {
        ('name_of_equip', CLASS_OF_EQUIP): {
            "config": {
                "cp": {
                    "inlet_cp_example": CLASS_OF_CONNECTION_POINT,
                    "other_cp_example": CLASS_OF_OTHER_CONNECTION_POINT
                },
                "properties": {
                    ("name_of_property", CLASS OF PROPERTY): {"optional_prop_of_property": PROP}
                }
                "relations": [
                    # list of relations
                ]
            }
        }
    }
}
```