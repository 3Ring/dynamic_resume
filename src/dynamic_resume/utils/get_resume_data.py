from pathlib import Path


def get_resume_data(path: Path) -> dict:

    if not path.exists():
        raise FileNotFoundError(f"YAML path {path} does not exist.")

    if not path.is_file():
        raise ValueError(f"YAML path {path} is not a file.")

    with open(path, "r") as f:
        if path.suffix in {".yml", ".yaml"}:
            import yaml

            data = yaml.safe_load(f)
        elif path.suffix == ".json":
            import json

            data = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

    if not isinstance(data, dict):
        raise ValueError(
            f"Invalid resume data format in {path}: expected a dictionary at the top level."
        )
    return data
