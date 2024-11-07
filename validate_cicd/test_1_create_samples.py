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
