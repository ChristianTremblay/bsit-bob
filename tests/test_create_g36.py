import os
import subprocess

import pytest


def test_create_g36(bob_fixture):
    samples_folder = bob_fixture["g36_directory"]
    samples_ttl_folder = bob_fixture["g36_ttl_directory"]
    for filename in os.scandir(samples_folder):
        if "broken" in filename.name:
            continue
        if filename.name.startswith("g36") and filename.name.endswith("py"):
            print("Making TTL")
            print(filename.path)
            assert not subprocess.call(["python", filename.path])


def test_create_html(bob_fixture):
    samples_folder = bob_fixture["g36_directory"]
    job = os.path.join(samples_folder, "ttl")
    assert not subprocess.call(["rdf2html", job])
