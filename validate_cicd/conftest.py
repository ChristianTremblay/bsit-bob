import glob
import os
from pathlib import Path

import pytest

from bob.core import clear

# Get the current script directory
current_dir = Path(__file__).resolve().parent.parent

# Construct the path to the ttl files
ttl_path = current_dir / "samples" / "conforming" / "**" / "ttl" / "*.compiled.ttl"
inferred_ttl_path = (
    current_dir
    / "samples"
    / "conforming"
    / "**"
    / "ttl"
    / "validation"
    / "*.compiled.ttl"
)
# print(ttl_path, current_dir)
# Use glob to find the files


def pytest_generate_tests(metafunc):
    if "data_file" in metafunc.fixturenames:
        args = glob.glob(str(ttl_path))
        # print(args)
        metafunc.parametrize("data_file", args)
    if "inferred_file" in metafunc.fixturenames:
        args = glob.glob(str(inferred_ttl_path))
        # print(args)
        metafunc.parametrize("inferred_file", args)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Be sure to clear graph after each test"""
    # Setup: fill with any logic you want

    yield  # this is where the testing happens

    clear()


@pytest.fixture(scope="session")
def bob_fixture(request):
    params = {}
    params["nonconforming_samples_directory"] = os.path.join(
        os.getcwd(), "samples", "nonconforming"
    )
    params["conforming_samples_directory"] = os.path.join(
        os.getcwd(), "samples", "conforming"
    )
    params["samples_ttl_directory"] = os.path.join(
        os.getcwd(), "samples", "nonconforming", "ttl"
    )
    params["g36_directory"] = os.path.join(os.getcwd(), "G36")
    params["g36_ttl_directory"] = os.path.join(os.getcwd(), "G36", "ttl")
    params["root_directory"] = os.path.join(os.getcwd())
    yield params
    # teardown
