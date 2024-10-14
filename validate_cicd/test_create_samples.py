import os
import subprocess
from pathlib import Path

import pytest

# @pytest.skip("Don't lose time with non-conforming samples")
# def test_build_nonconforming_samples(bob_fixture):
#    samples_folder = bob_fixture["nonconforming_samples_directory"]
#    for root, dirs, files in os.walk(samples_folder):
#        for filename in os.scandir(Path(root)):
#            if filename.name.startswith("sample") and filename.name.endswith("py"):
#                assert not subprocess.call(["python", filename.path])


def test_build_conforming_samples(bob_fixture):
    samples_folder = bob_fixture["conforming_samples_directory"]
    for root, dirs, files in os.walk(samples_folder):
        if "src" in dirs:
            src_folder = Path(root) / "src"
            for filename in os.scandir(src_folder):
                if filename.name.startswith("sample") and filename.name.endswith("py"):
                    assert not subprocess.call(["python", filename.path])


def test_create_html(bob_fixture):
    samples_folder = bob_fixture["conforming_samples_directory"]
    for root, dirs, files in os.walk(samples_folder):
        if "ttl" in dirs:
            ttl_folder = Path(root) / "ttl"
            assert not subprocess.call(["rdf2html", ttl_folder.resolve(), "--move"])


def test_compile_conforming_samples(bob_fixture):
    samples_folder = bob_fixture["conforming_samples_directory"]
    for root, dirs, files in os.walk(samples_folder):
        if "ttl" in dirs:
            ttl_folder = Path(root) / "ttl"
            assert not subprocess.call(["compile_ttl", ttl_folder.resolve()])


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
                    _queries.append(filename.path)
        if "ttl" in dirs:
            ttl_folder = Path(root) / "ttl"
            for filename in os.scandir(ttl_folder):
                if filename.name.endswith("compiled.ttl"):
                    _model = filename.path
    assert not subprocess.call(["query_model", _model, rq_folder, "--move"])
