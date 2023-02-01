# flake8: noqa

#
#   Project Metadata
#

__version__ = "0.68"
__author__ = "Joel Bender"
__email__ = "jjb5@cornell.edu"

# basic pieces for all Bob models
from .core import (
    data_graph,  # the data model created
    schema_graph,  # the schema for the custom components in the model
    bind_model_namespace,  # associate a namespace and prefix
    dump,  # output a graph, defaults to data_graph
    Node,  # a node in a graph
)

# core classes for S223 models
from .core import (
    Equipment,  # a piece of equipment
    System,  # a collection of equipment
    PhysicalSpace,  # heirarchy of things like building, floor, room
    DomainSpace,  # portion of a physical space for a specific domain
    Zone,  # collections of domain spaces
)
