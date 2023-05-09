s223_types = {
    "Equipment": ["s223:Equipment"],
    "Connection": ["s223:Connection"],
    #'s223': ["s223"],
    "InletConnectionPoint": [
        "s223:InletConnectionPoint",
        "s223:InletConnectionPoint",
        "p223:ProducerInput",
        "s223:BidirectionalConnectionPoint",
    ],
    "OutletConnectionPoint": [
        "s223:OutletConnectionPoint",
        "s223:FunctionOutput",
        "p223:ProducerOutput",
    ],
    "FunctionBlock": ["p223:Producer", "s223:FunctionBlock"],
    "DomainSpace": ["s223:DomainSpace", "s223:PhysicalSpace"],
}

propgraph_labels = {
    "value": ["hasValue"],
    "direction": ["hasDirection"],
    "aspects": ["hasAspects"],
    "medium": ["hasMedium", "ofSubstance", "ofMedium"],
    "quantityKind": ["hasQuantityKind"],
    "enumerationKind": ["hasEnumerationKind"],
    "domain": ["hasDomain"],
    "unit": ["qudt/unit", "vocab/unit"],
}

bacnet_labels = {
    "object-identifier": "http://data.ashrae.org/bacnet/2020#object-identifier",
    "object_type": "http://data.ashrae.org/bacnet/2020#object-type",
    "object-name": "http://data.ashrae.org/bacnet/2020#object-name",
    "description": "http://data.ashrae.org/bacnet/2020#description",
    "address": "http://data.ashrae.org/bacnet/2020#address",
    "device-name": "http://data.ashrae.org/bacnet/2020#device-name",
    "device-identifier": "http://data.ashrae.org/bacnet/2020#device-identifier",
    "vendor-identifier": "http://data.ashrae.org/bacnet/2020#vendor-identifier",
    "vendor-name": "http://data.ashrae.org/bacnet/2020#vendor-name",
    "network-number": "http://data.ashrae.org/bacnet/2020#network-number",
}

skip_edges = [
    "label",
    "comment",
    "hasDirection",
    "ns#type",
    "hasValue",
    "hasAspect",
    "hasMedium",
    "hasQuantityKind",
    "ofMedium",
    "ofSubstance",
    "hasEnumerationKind",
    "hasDomain",
    "vocab/unit",
    "qudt/unit",
    "2020#object-identifier",
    "2020#object-type",
    "2020#object-name",
    "2020#description",
    "2020#address",
    "2020#device-name",
    "2020#device-identifier",
    "2020#vendor-identifier",
    "2020#vendor-name",
    "2020#network-number",
]


def is_wanted_node(predicate):
    for each in skip_edges:
        if each in predicate:
            return False
    return True
