import pytest
from bob.core import clear


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Be sure to clear graph after each test"""
    # Setup: fill with any logic you want

    yield  # this is where the testing happens

    clear()
