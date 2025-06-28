import copy
import re
import typing as t
from pathlib import Path

import yaml

from . import schemaorg
from .core import (
    BoundaryConnectionPoint,
    Connection,
    ConnectionPoint,
    Equipment,
    System,
)
from .introspection import get_class_from_name


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
    # print('Looking for : ', container, blob)
    if "[" in blob:
        matches = re.findall(r'\[["\'](.*?)["\']\]', blob)  # sub-equipment
        property_match = re.search(
            r"\.(?P<property>\w+)$", blob
        )  # property => .something
        thing = container[matches.pop(0)]

        for each in matches:
            thing = thing[each]
        # print('thing : ', thing, property_match)
        if property_match:
            property_name = property_match.group("property")
            # try:
            #
            #    thing_property = getattr(thing, property_name)
            #    if thing_property is None:
            #        thing_property = thing # in case thing_property is None, we give the part before .something
            # except AttributeError:
            #    thing_property = None
            # print(thing_property, property_name)
            return (thing, property_name)  # in case thing_property is None
        # print(thing, None)
        return (thing, None)
    else:
        _key = blob.split(".")[1]
        thing = getattr(container, _key)
        # print(thing, _key)
        return (thing, _key)  # in case thing is None


def configure_boundaries(container: System, boundaries: t.List[t.Tuple[str, str]]):
    for _target in boundaries:
        target_element, target_key = get_instance(container, _target)

        if target_key is None:
            target = target_element
        else:
            target = getattr(target_element, target_key, None)

        if target is None and isinstance(target_element, ConnectionPoint):
            target = target_element
        elif target is None:
            raise AttributeError(f"Target {target_key} not found in {target_element}")

        container | target


def configure_relations(
    container: t.Union[Equipment, System], relations: t.List[t.Tuple[str, str, str]]
):
    for relation in relations:
        _source, operator, _target = relation
        source_element, source_key = get_instance(container, _source)
        target_element, target_key = get_instance(container, _target)

        if source_key is None:
            source = source_element
        else:
            source = getattr(source_element, source_key, None)
        if source is None and isinstance(source_element, Connection):
            source = source_element

        # if source_element is None:
        #    source_element = container

        # if source_key is None:
        #    source = source_element
        # else:
        #    source = getattr(source_element, source_key, None)

        # if source is None and isinstance(source_element, Connection):
        #    source = source_element
        # elif source is None:
        #    raise AttributeError(f"Source {source_key} not found in {source_element} | container {container} | relation {relation}")

        if target_key is None:
            target = target_element
        else:
            target = getattr(target_element, target_key, None)

        if target is None and isinstance(target_element, Connection):
            target = target_element
        elif target is None:
            raise AttributeError(f"Target {target_key} not found in {target_element}")

        if operator == "=":
            if source is None:
                # print(equipment, source_key, target)
                try:
                    setattr(source_element, source_key, target)
                except AttributeError:
                    setattr(container, source_key, target)
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
        elif operator == "mapsTo":
            source.mapsTo = target
        elif operator == "@":
            source @ target
        elif operator == "|":
            source | target
        # no @ here as we are creating relation "inside" the equipment or system


class SystemFromTemplate(System):
    def __init__(self, config: t.Dict = None, **kwargs):
        required_class = config.pop("template_class")
        _config = template_update(config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        if not issubclass(required_class, System):
            raise TypeError(
                f"template_class {required_class} must be a subclass of System"
            )
        _relations = _config.pop("relations", [])
        _boundaries = _config.pop("boundaries", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        configure_boundaries(self, _boundaries)


class ProductGroupFromTemplate(SystemFromTemplate, schemaorg.ProductGroup):
    """
    A class to create a product group from a template.
    It inherits from SystemFromTemplate and allows to create a Schema.org
    product group with the same configuration as the system.
    """

    def __init__(self, config: t.Dict = None, **kwargs):
        super().__init__(config, **kwargs)


class EquipmentFromTemplate(Equipment):
    def __init__(self, config: t.Dict = None, **kwargs):
        required_class = config.pop("template_class")
        _config = template_update(config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        
        if required_class is System:
            raise TypeError(
                "EquipmentFromTemplate should not be used with System as template_class. Use SystemFromTemplate instead."
            )
        elif not issubclass(required_class, Equipment):
            raise TypeError(
                f"template_class {required_class} must be a subclass of Equipment"
            )
        # Class mutation
        self.__class__ = required_class
        required_class.__init__(self, _config, **kwargs)
        configure_relations(self, _relations)
        # configure_mapsTo(self, _mapsTo)


class ProductFromTemplate(EquipmentFromTemplate, schemaorg.Product):
    def __init__(self, config: t.Dict = None, **kwargs):
        super().__init__(config, **kwargs)


def config_from_yaml(yaml_file: t.Union[str, Path, t.Dict] = None):
    if yaml_file is None:
        raise FileNotFoundError("No YAML file provided")
    else:
        if isinstance(yaml_file, dict):
            yaml_content = yaml_file
        else:
            yaml_file = Path(yaml_file)
            if not yaml_file.is_file():
                raise FileNotFoundError(f"YAML file {yaml_file} not found")
            with open(yaml_file, "r") as file:
                yaml_content = yaml.safe_load(file)
    _text_values = ["label", "comment"]
    _dict = {}
    name = yaml_content["name"]
    params = yaml_content["params"]
    template_class = (
        get_class_from_name(yaml_content["template_class"]) if "template_class" in yaml_content else System
    )
    _dict['template_class'] = template_class

    label = params.get("label", name)
    comment = params.get("comment", "")
    sensors = yaml_content.get("sensors", None)
    equipment = yaml_content.get("equipment", None)
    connections = yaml_content.get("connections", None)
    junctions = yaml_content.get("junctions", None)
    connection_points = yaml_content.get("cp", None)

    # boundaries = yaml_content.get("boundaries", None)

    _dict["params"] = {"label": label, "comment": comment}
    # Schema.org parameters treated as kwargs
    _dict["params"].update(yaml_content.get("schemaorg", {}))

    def define_entities(entities: dict = None, entities_category: str = None):
        if entities is None:
            return
        _dict[entities_category] = {}
        if entities_category == "cp":
            for entity_name, _entity_class in entities.items():
                # entity_label = entity_params['label'] if 'label' in entity_params else entity_name
                entity_class = get_class_from_name(_entity_class)
                entity_label = entity_name
                # ConnectionPoint
                _dict[entities_category][entity_label] = entity_class
        else:
            for entity_name, entity_params in entities.items():
                # entity_label = entity_params['label'] if 'label' in entity_params else entity_name
                entity_label = entity_params.pop("label", entity_name)
                # print(entity_label, entity_params, f"Looking for {entity_params['class']}")
                try:
                    entity_class = get_class_from_name(entity_params.pop("class"))
                except KeyError:
                    raise KeyError(
                        f"Entity {entity_name} in {entities_category} does not have a 'class' key"
                    )
                # print('Found class', entity_class)
                # entity_comment = entity_params.pop('comment', '')

                else:
                    _dict[entities_category][(entity_label, entity_class)] = {}
                    for _name, _class_or_value in entity_params.items():
                        _value = (
                            _class_or_value
                            if _name in _text_values
                            else get_class_from_name(_class_or_value)
                        )
                        _dict[entities_category][(entity_label, entity_class)][
                            _name
                        ] = _value

    # print('Defining entities')
    define_entities(equipment, "equipment")
    define_entities(sensors, "sensors")
    define_entities(connections, "connections")
    define_entities(junctions, "junctions")
    if connection_points is not None:
        define_entities(connection_points, "cp")
    # define_entities(boundaries, "boundaries")
    _dict["relations"] = []
    if template_class is System:
        _dict["boundaries"] = []

    def parse_sub(a):
        if "." in a:
            main, sub = a.split(".")
            return f"self['{main.strip()}'].{sub.strip()}"
        else:
            return f"self['{a.strip()}']"

    def add_to_relation_dict(line, operator, separator=","):
        line = line.replace("(", "").replace(")", "").strip()
        _a, _b = line.split(separator)
        _dict["relations"].append((parse_sub(_a), operator, parse_sub(_b)))
        # print(parse_sub(_a), operator, parse_sub(_b))

    # Explicit relations with operator in the yaml file
    _relations = yaml_content.get("relations", [])
    for _relation in _relations:
        add_to_relation_dict(_relation, ">>", separator=",")

    # Relations using label, no self, no operator (implicit >>)
    # Generalize handling of all *_connections sections
    for key, value in yaml_content.items():
        if re.match(r".*_connections$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, ">>", separator=" -> ")

    for key, value in yaml_content.items():
        if re.match(r".*mapsTo$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "mapsTo", separator=" -> ")

    # observation location
    observation_location = yaml_content.get("sensors_observation_location", [])
    for _observations in observation_location:
        add_to_relation_dict(_observations, "%", separator=" -> ")
    boundaries = yaml_content.get("boundaries", [])
    for _boundary in boundaries:
        # add_to_relation_dict(_boundary, "|", separator=" -> ")
        _dict["boundaries"].append(f"self | {parse_sub(_boundary)}")
    return _dict
