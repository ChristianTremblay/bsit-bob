# flake8: noqa

#
#   Project Metadata
#
import os
from multiprocessing import connection
from typing import Any, Dict, TypeVar, Union

from rdflib import URIRef

__version__ = "0.37"
__author__ = "Joel Bender"
__email__ = "jjb5@cornell.edu"

try:
    if os.path.isfile("{}/.env".format(os.getcwd())):
        from dotenv import load_dotenv

        load_dotenv(os.path.join(os.getcwd(), ".env"))
except ImportError:
    print("You need to pip install python-dotenv to use your .env file")
