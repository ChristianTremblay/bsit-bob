from asyncio import subprocess
import pytest
import os
import subprocess
from bob.core import clear
import logging

LOGGER = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Be sure to clear graph after each test"""
    # Setup: fill with any logic you want

    yield  # this is where the testing happens

    clear()


@pytest.fixture(scope="session")
def bob_fixture(request):
    print("\nDoing setup")
    params = {}
    params["samples_directory"] = os.path.join(os.getcwd(), "samples")
    params["samples_ttl_directory"] = os.path.join(os.getcwd(), "samples", "ttl")
    params["g36_directory"] = os.path.join(os.getcwd(), "G36")
    params["g36_ttl_directory"] = os.path.join(os.getcwd(), "G36", "ttl")
    yield params
    # teardown
