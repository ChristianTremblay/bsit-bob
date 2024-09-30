import glob
import logging
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import ontoenv
import rdflib
from dotenv import load_dotenv

load_dotenv()
S223_FOLDER = Path(os.getenv("S223_FOLDER"))
current_dir = Path(__file__).resolve().parent.parent


def main():
    # Construct the path to the ttl files
    base_folder = current_dir / "samples" / "ttl" / "validation"
    print(f"Base Folder : {base_folder}")

    # Define the folder paths and other TTL files to be merged
    other_ttl_files = []
    other_ttl_files.extend(
        glob.glob(
            os.path.join(
                S223_FOLDER, "imports/qudt/VOCAB_QUDT-QUANTITY-KINDS-ALL-v2.1.ttl"
            )
        )
    )
    other_ttl_files.extend(
        glob.glob(
            os.path.join(S223_FOLDER, "imports/qudt/VOCAB_QUDT-UNITS-ALL-v2.1.ttl")
        )
    )
    other_ttl_files.extend(glob.glob(os.path.join(S223_FOLDER, "models/*.ttl")))
    other_ttl_files.extend(glob.glob(os.path.join(S223_FOLDER, "vocab/*.ttl")))
    other_ttl_files.extend(glob.glob(os.path.join(S223_FOLDER, "validation/*.ttl")))
    other_ttl_files.extend(glob.glob(os.path.join(S223_FOLDER, "inference/*.ttl")))

    # Find all .data.ttl and .schema.ttl files
    data_files = glob.glob(os.path.join(base_folder, "*.data.ttl"))
    schema_files = glob.glob(os.path.join(base_folder, "*.schema.ttl"))

    # Group files by prefix
    files_by_prefix = defaultdict(list)
    for file in data_files + schema_files:
        prefix = os.path.basename(file).rsplit(".", 2)[0]
        files_by_prefix[prefix].append(file)

    print(f"Files by Prefix : {files_by_prefix}")
    # Merge files with the same prefix along with other specified TTL files
    for prefix, files in files_by_prefix.items():
        print(f"Prefix : {prefix}")
        output_file = base_folder / f"{prefix}.compiled.ttl"
        command = (
            [
                "python3",
                str(current_dir / "validate_cicd/merge-graphs.py"),
                "--no-imports",
                "--clean",
            ]
            + files
            + other_ttl_files
            + [output_file]
        )
        print(command)
        subprocess.run(command)


if __name__ == "__main__":
    main()
