from pathlib import Path
from uuid import uuid4


GENERATED_FILES_DIR = Path(__file__).resolve().parent.parent / "generated_files"
GENERATED_FILES_DIR.mkdir(exist_ok=True)


def make_output_filename(model_type: str) -> str:
    return f"{model_type}-{uuid4().hex}.step"


def get_output_file_path(filename: str) -> Path:
    return GENERATED_FILES_DIR / filename
