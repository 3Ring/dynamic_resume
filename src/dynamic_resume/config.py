import typing as t
from pathlib import Path
from os import PathLike

DEFAULT_TEMPLATE_PATH: Path = Path(__file__).parent / "templates"
TEMPLATE_PATH: Path = DEFAULT_TEMPLATE_PATH / "swe_resume.j2"
DATA_PATH: t.Optional[Path] = None


def set_template_path(path: str | PathLike) -> None:
    j2_path = Path(path).expanduser().resolve()

    if not j2_path.exists():
        raise FileNotFoundError(f"Template path {j2_path} does not exist.")

    if not j2_path.is_file():
        raise ValueError(f"Template path {j2_path} is not a file.")

    if j2_path.suffix not in {".j2", ".jinja2"}:
        raise ValueError(f"Template path {j2_path} is not a Jinja2 template file.")

    global TEMPLATE_PATH
    TEMPLATE_PATH = j2_path


def set_data_path(path: str | PathLike) -> None:
    data_path = Path(path).expanduser().resolve()

    if not data_path.exists():
        raise FileNotFoundError(f"Data path {data_path} does not exist.")
    if not data_path.is_file():
        raise ValueError(f"Data path {data_path} is not a file.")

    if data_path.suffix not in {".yml", ".yaml", ".json"}:
        raise ValueError(f"Data path {data_path} is not a YAML or JSON file.")

    global DATA_PATH
    DATA_PATH = data_path
