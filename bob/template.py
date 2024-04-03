import typing as t
from bob.core import Equipment, System
import re
import copy


def template_update(base: t.Dict = {}, config: t.Dict = None, bases: t.List = None):
    """
    This utility allows to preserve module templates from
    undesired modification during creation of Equipment.

    Usage :
    _config = template_update(template, user_provided_config_dict)

    """

    def merge_dict(existing, new):
        for k in new:
            if k in existing:
                if isinstance(existing[k], dict) and isinstance(new[k], dict):
                    merge_dict(existing[k], new[k])
                else:
                    existing[k] = new[k]
            else:
                existing[k] = new[k]

    if bases:
        d1, d2 = bases
        _d1 = copy.deepcopy(d1)
        _d2 = copy.deepcopy(d2)
        merge_dict(_d1, _d2)
        if config:
            merge_dict(_d1, config)
        return _d1

    else:
        _d = copy.deepcopy(base)
        if config:
            merge_dict(_d, config)
        return _d


def get_instance(container: t.Union[Equipment, System], blob: str):
    print('Looking for : ', container, blob)
    if "[" in blob:
        matches = re.findall(r'\[["\'](.*?)["\']\]', blob) # sub-equipment
        property_match = re.search(r"\.(?P<property>\w+)$", blob) # property => .something
        thing = container[matches.pop(0)]
        
        for each in matches:
            thing = thing[each]
        print('thing : ', thing, property_match)
        if property_match:
            property_name = property_match.group("property")
            #try:
            #    
            #    thing_property = getattr(thing, property_name)
            #    if thing_property is None:
            #        thing_property = thing # in case thing_property is None, we give the part before .something
            #except AttributeError:
            #    thing_property = None
            #print(thing_property, property_name)
            return (thing, property_name)  # in case thing_property is None
        #print(thing, None)
        return (thing, None)
    else:
        _key = blob.split(".")[1]
        thing = getattr(container, _key)
        #print(thing, _key)
        return (thing, _key)  # in case thing is None


def configure_relations(
    container: t.Union[Equipment, System], relations: t.List[t.Tuple[str, str, str]]
):
    for relation in relations:
        _source, operator, _target = relation
        source_element, source_key = get_instance(container, _source)
        target_element, target_key = get_instance(container, _target)
        
        source = getattr(source_element, source_key, None)
        if target_key is None:
            target = target_element
        else:
            target = getattr(target_element, target_key, None)

        if target is None:
            raise AttributeError(f"Target {target_key} not found in {target_element}")

        if operator == "=":
            if source is None:
                # print(equipment, source_key, target)
                try:
                    setattr(source_element, source_key, target)
                except TypeError as error:
                    print(error)
                    print("Container :", container)
                    print("Source :", source, source_key)
                    print("Target :", target, target_key)

            else:
                source = target
        elif operator == ">>":
            source >> target
        elif operator == "<<":
            source << target
        elif operator == "%":
            source % target
        # no @ here as we are creating relation "inside" the equipment or system


class SystemFromTemplate(System):
    def __init__(self, config: t.Dict = None, **kwargs):
        _config = template_update(config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
