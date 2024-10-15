import os
import shutil
from pathlib import Path

from .core import data_graph, dump, schema_graph
from .scratch.header import sample_header


def create_data_and_schema_ttl(
    model_name: str = None, folder: Path = None, header: str = None
):

    if model_name is None:
        raise ValueError("model_name is required")

    if folder is None:
        folder = Path(__file__).parent

    if header is None:
        header = sample_header(model_name, "data")

    dump(
        data_graph,
        filename=f"{folder}/{model_name}.data.ttl",
        header=sample_header(model_name, "data"),
    )
    dump(
        schema_graph,
        filename=f"{folder}/{model_name}.schema.ttl",
        header=sample_header(model_name, "schema"),
    )

    ttl_folder = folder.parent / "ttl"

    if ttl_folder.exists():
        try:
            os.remove(f"{ttl_folder}/{model_name}.data.ttl")
            os.remove(f"{ttl_folder}/{model_name}.schema.ttl")
        except FileNotFoundError:
            pass
        shutil.move(src=f"{folder}/{model_name}.schema.ttl", dst=ttl_folder)
        shutil.move(src=f"{folder}/{model_name}.data.ttl", dst=ttl_folder)


def model_namespace(file: Path = None):
    if Path(file).parent.stem == "src":
        model_name = Path(file).stem
        global_ns = Path(file).parent.parent.stem
    else:
        model_name = Path(file).stem
        global_ns = Path(file).parent.stem
    # _namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")
    return (model_name, global_ns)
