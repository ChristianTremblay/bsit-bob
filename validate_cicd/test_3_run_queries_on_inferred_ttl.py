import os
import subprocess
from pathlib import Path

import pytest


def test_query_conforming_samples(bob_fixture):
    samples_folder = bob_fixture["conforming_samples_directory"]
    _queries = []
    _model = None
    ttl_folder = None
    rq_folder = None
    for root, dirs, files in os.walk(samples_folder):
        if "sparql" in dirs:
            rq_folder = Path(root) / "sparql"
            for filename in os.scandir(rq_folder):
                if filename.name.endswith("rq"):
                    print(filename.path)
                    _queries.append(filename.path)
        if "ttl" in dirs:
            ttl_folder = Path(root) / "ttl" / "validation"
            for filename in os.scandir(ttl_folder):
                if filename.name.endswith("compiled.ttl"):
                    print(filename.path)
                    _model = filename.path
    assert _model is not None
    assert ttl_folder is not None
    assert rq_folder is not None

    assert not subprocess.call(["query_model", _model, rq_folder, "--move"])
