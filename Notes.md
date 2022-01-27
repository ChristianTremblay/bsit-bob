# hasUnits vs hasUnit

hasUnits -> hasUnit

Schema in 223 hasUnits... everywhere : hasUnit

# ExternalDataSource
I need that for my model so I start by making a super simple class that 
will be subclassed in the future.
For now I use hasSimpleLink to store the datasource


In the model I need the creation of 

s223:ExternalDataSource
s223:isExternalDataSourceOf -> Property

## Weird trouble
Can't understand why `isValueOf` gets its class "Property"
But `isExternalDataSourceOf` can't...
ended up with this really ugly exception 

    # node.py line 378
    if isinstance(self._nodes[attr], str):
        node_class = _annotation_reference.get(self._nodes[attr], None)  # type: ignore[arg-type]
        if not node_class:
            raise NotImplementedError(
                f"class {self._nodes[attr]!r} for attribute {attr!r} not found"
            )
        self._nodes[attr] = node_class
    elif not self._nodes[attr]:
        # This is weird case for isExternalDataSourceOf.
        # Where even if it's typed as Property
        # it's not working...
        if attr == 'isExternalDataSourceOf':
            node_class = Property
            self._nodes[attr]

# Measures
When creating sensors, we need a property 
Added TemperatureMeasure, a property observed by the sensor
On this property, I  add the external datasource


# Substance NaturalGas


