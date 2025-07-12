import copy
import re
import typing as t
from pathlib import Path
import importlib
import warnings

import yaml

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
        #try:
        thing = getattr(container, _key)
        #except AttributeError:
        #    thing = container[_key]
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
        elif source is None:
            try:
                source = source_element[source_key]
            except KeyError:
                raise AttributeError(f"Source {source_key} not found in {source_element}")

        if target_key is None:
            target = target_element
        else:
            target = getattr(target_element, target_key, None)

        if target is None and isinstance(target_element, Connection):
            target = target_element
        elif target is None:
            try:
                target = target_element[target_key]
            except KeyError:
                raise AttributeError(f"Target {target_key} not found in {target_element}")

        print(f"Configuring relation: {source} {operator} {target}")


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
            source.maps_to(target)
        elif operator == "@":
            source @ target
        elif operator == "|":
            source | target
        elif operator == "executes":
            source.executes(target)
        elif operator == "hasInput":
            source.hasInput(target)
        elif operator == "hasOutput":
            source.hasOutput(target)


class SystemFromTemplate(System):
    def __init__(self, config: t.Dict = None, **kwargs):
        required_class = (
            config.pop("template_class") if "template_class" in config else [System]
        )

        _config = template_update(config)
        kwargs = {**_config.pop("params", {}), **kwargs}

        _relations = _config.pop("relations", [])
        _boundaries = _config.pop("boundaries", [])

        # Class mutation, we want a more explicit System maybe (ex. schema.org ProductGroup)...
        _tuple = (
            tuple(required_class) + (System,)
            if System not in required_class
            else tuple(required_class)
        )
        DynamicClass = type(
            f"Dynamic{'_'.join(cls.__name__ for cls in required_class)}",
            _tuple,
            {},
        )
        self.__class__ = DynamicClass

        DynamicClass.__init__(self, _config, **kwargs)

        configure_relations(self, _relations)
        configure_boundaries(self, _boundaries)


class EquipmentFromTemplate(Equipment):
    def __init__(self, config: t.Dict = None, **kwargs):
        required_class = (
            config.pop("template_class") if "template_class" in config else Equipment
        )
        _config = template_update(config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])

        # Class mutation, we want a more explicit Equipment maybe...
        _tuple = (
            tuple(required_class) + (Equipment,)
            if Equipment not in required_class
            else tuple(required_class)
        )
        DynamicClass = type(
            f"Dynamic{'_'.join(cls.__name__ for cls in required_class)}",
            _tuple,
            {},
        )
        self.__class__ = DynamicClass

        DynamicClass.__init__(self, _config, **kwargs)

        configure_relations(self, _relations)


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
    _text_values = ["label", "comment", "hasValue", "config", "vendorIdentifier", "objectIdentifier", "objectName", "description"]
    _dict = {}
    name = yaml_content["name"]
    params = yaml_content["params"]
    _template_class = yaml_content["template_class"]
    template_class = []
    if isinstance(_template_class, list):
        for each in _template_class:
            template_class.append(get_class_from_name(each))
    else:
        template_class.append(get_class_from_name(_template_class))
    _dict["template_class"] = template_class

    label = params.get("label", name)
    comment = params.get("comment", "")
    sensors = yaml_content.get("sensors", {})
    equipment = yaml_content.get("equipment", {})
    properties = yaml_content.get("properties", {})
    functions = yaml_content.get("functions", {})
    connections = yaml_content.get("connections", {})
    junctions = yaml_content.get("junctions", {})
    connection_points = yaml_content.get("cp", {})
    bacnet = yaml_content.get("bacnet", {})
    influxdb = yaml_content.get("influxdb", {})

    # boundaries = yaml_content.get("boundaries", None)

    _dict["params"] = {"label": label, "comment": comment}
    # Schema.org parameters treated as kwargs
    try:
        for key, value in yaml_content.items():
            if key.startswith("params_"):
                class_name = key.split("params_")[-1]
                package = value.pop("package", None)
                if package is None:
                    raise KeyError(
                        f"params_{class_name} must have a 'package' key to be imported"
                    )
                try:
                    module = importlib.import_module(package)
                    cls = getattr(module, class_name)
                except ImportError as e:
                    raise ImportError(
                        f"Could not import package '{package}' for params_{class_name}: {e}, parameters not supported."
                    )
                _dict["params"].update(value)
    except ImportError as e:
        warnings.warn(
            f"Could not import parameters from YAML file: {e}. Parameters will not be applied."
        )

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
                        # Here maybe I could look for hasattr in the class to check if the attribute exists and use its value
                        _dict[entities_category][(entity_label, entity_class)][
                            _name
                        ] = _value

    # print('Defining entities')
    define_entities(equipment, "equipment")
    define_entities(properties, "properties")
    define_entities(sensors, "sensors")
    define_entities(connections, "connections")
    define_entities(junctions, "junctions")
    if connection_points is not None:
        define_entities(connection_points, "cp")
    # define_entities(boundaries, "boundaries")
    from_catalog = yaml_content.get("from_catalog", None)

    if from_catalog is not None:
        catalog_module, catalog_lookup_function = yaml_content.get(
            "catalog_source", ""
        ).split("|")
        importlib.import_module(catalog_module)
        get_template = getattr(
            importlib.import_module(catalog_module), catalog_lookup_function
        )



        for entity_name, entity_params in from_catalog.items():
            # entity_label = entity_params['label'] if 'label' in entity_params else entity_name
            entity_label = entity_params.pop("label", entity_name)
            # print(entity_label, entity_params, f"Looking for {entity_params['template']}")
            _template = entity_params.pop("template")
            _addon = entity_params.pop("addon", None)
            try:
                template = get_template(_template)
            except FileNotFoundError:
                # maybe it's a file
                if not Path(_template).is_file():
                    raise FileNotFoundError(
                        f"Template {entity_name} not found in catalog {catalog_module}"
                    )
                else:
                    template = _template

            try:
                if _addon is not None:
                    with open(Path(_addon)) as _addon_file:
                        _addon_dict = yaml.safe_load(_addon_file)
                    template = template_update(template, _addon_dict)
                    
                _template_config = config_from_yaml(
                    template
                )

                if "System" in _template_config["template_class"]:
                    _dict["equipment"][(entity_label, SystemFromTemplate)] = {
                        "config": _template_config
                    }
                else:
                    _dict["equipment"][(entity_label, EquipmentFromTemplate)] = {
                        "config": _template_config
                    }

            except KeyError:
                raise KeyError(
                    f"Entity {entity_name} in equipment_from_catalog does not have a 'template' key"
                )
    define_entities(bacnet, "bacnet")
    define_entities(functions, "functions")
    

    _dict["relations"] = []
    if template_class[0] is System:
        _dict["boundaries"] = []

    def parse_sub(a, include_self=True):
        parts = [p.strip() for p in a.split(".")]
        if not include_self:
            expr = f"[{parts[0]}]"
        else:
            expr = f"self['{parts[0]}']"
        for part in parts[1:]:
            expr += f".{part}"
        return expr

    def parse_sub_properties(a):
        parts = [p.strip() for p in a.split(" / ")]
        expr = f"self['{parts[0]}']"
        for part in parts[1:]:
            expr += f"{parse_sub(part, include_self=False)}"
        return expr

    def add_to_relation_dict(line, operator, separator=","):
        line = line.replace("(", "").replace(")", "").strip()
        _a, _b = line.split(separator)
        _dict["relations"].append((parse_sub(_a), operator, parse_sub(_b)))
        # print(parse_sub(_a), operator, parse_sub(_b))

    def add_reference_to_relation_dict(line, operator, separator=","):
        """
        References are using properties which are accessed using the square brackets
        instead of the dot notation.
        In the template, we are using " / " to separate the property name
        from the object name.
        Keeping the parse_sub option for the last part as we can have the need to 
        access a property of the property, like the bacnet presentValue.
        """
        line = line.replace("(", "").replace(")", "").strip()
        _a, _b = line.split(separator)
        _dict["relations"].append((parse_sub_properties(_a), operator, parse_sub_properties(_b)))
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

        if re.match(r".*mapsTo$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "mapsTo", separator=" -> ")

        if re.match(r".*_executes$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "executes", separator=" -> ")
        if re.match(r".*functions_inputs$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "hasInput", separator=" -> ")

        if re.match(r".*functions_outputs$", key) and isinstance(value, list):
            for _connection in value:
                add_to_relation_dict(_connection, "hasOutput", separator=" -> ")
        if re.match(r".*_references$", key) and isinstance(value, list):
            for _connection in value:
                print(f"Adding reference to relation dict: {_connection}")
                add_to_relation_dict(
                    _connection, "@", separator=" -> "
                )

    # observation location
    observation_location = yaml_content.get("sensors_observation_location", [])
    for _observations in observation_location:
        add_to_relation_dict(f"{_observations}", "%", separator=" -> ")
    boundaries = yaml_content.get("boundaries", [])
    for _boundary in boundaries:
        # add_to_relation_dict(_boundary, "|", separator=" -> ")
        _dict["boundaries"].append(f"self | {parse_sub(_boundary)}")
    return _dict
