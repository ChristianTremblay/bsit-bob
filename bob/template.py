import typing as t
from bob.core import Equipment
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

def get_instance(equipment:Equipment, blob:str):
        
        if "self." in blob:
            _key = blob.split('.')[1]
            thing = getattr(equipment, _key)
            #print('Simple ', equipment, thing, _key)
            return (thing, _key) # in case thing is None
        if 'self[' in blob:
            matches = re.findall(r'\["(.*?)"\]', blob)
            property_match = re.search(r'\.(?P<property>\w+)$', blob)
            thing = equipment[matches.pop(0)]
            for each in matches:
                thing = thing[each]
            if property_match:
                property_name = property_match.group('property')
                thing_property = getattr(thing, property_name)
                #print('Complex.property ', equipment, thing_property, property_name)
                return (thing_property, property_name) # in case thing_property is None
            #print('Complex ', equipment, thing, None)
            return (thing, None)

def configure_relations(equipment:Equipment, relations:t.List[t.Tuple[str,str,str]]):
    for relation in relations:
        _source, operator, _target = relation
        source, source_key = get_instance(equipment, _source)
        target, target_key = get_instance(equipment, _target)
        if operator == "=":
            if source is None:
                #print(equipment, source_key, target)
                try:
                    setattr(equipment, source_key, target)
                except TypeError as error:
                    print(error)
                    print('Equipment :', equipment)
                    print('Source :', source, source_key)
                    print('Target :', target, target_key)

            else:
                source = target
        elif operator == ">>":
            source >> target
        elif operator == "<<":
            source << target
        elif operator == "%":
            source % target
        # no @ here as we are creating relation "inside" the equipment