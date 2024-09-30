import glob
from pathlib import Path

# Get the current script directory
current_dir = Path(__file__).resolve().parent.parent

# Construct the path to the ttl files
ttl_path = current_dir / "samples" / "ttl" / "validation" / "*.compiled.ttl"
# print(ttl_path, current_dir)
# Use glob to find the files


def pytest_generate_tests(metafunc):
    if "data_file" in metafunc.fixturenames:
        args = glob.glob(str(ttl_path))
        # print(args)
        metafunc.parametrize("data_file", args)
