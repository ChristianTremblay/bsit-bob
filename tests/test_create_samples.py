import os
import subprocess

import pytest


def test_create_samples(bob_fixture):
    samples_folder = bob_fixture["samples_directory"]
    samples_ttl_folder = bob_fixture["samples_ttl_directory"]
    for filename in os.scandir(samples_folder):
        if "broken" in filename.name:
            continue
        if filename.name.startswith("sample") and filename.name.endswith("py"):
            print("Making TTL")
            print(filename.path)
            assert not subprocess.call(["python", filename.path])


def test_build_pritoni_samples(bob_fixture):
    samples_folder = os.path.join(bob_fixture["samples_directory"], "sample_pritoni")
    samples_ttl_folder = bob_fixture["samples_ttl_directory"]
    filename = os.path.join(samples_folder, "sample_pritoni_model.py")
    assert not subprocess.call(["python", filename])


def test_create_html(bob_fixture):
    samples_folder = bob_fixture["samples_directory"]
    job = os.path.join(samples_folder, "create_html.py")
    assert not subprocess.call(["python", job])
