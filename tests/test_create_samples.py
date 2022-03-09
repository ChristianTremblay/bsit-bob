import pytest
import os
import subprocess


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
