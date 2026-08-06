from pathlib import Path

from config import MAX_CHARS_TO_SEND_TO_LLM
from utils.file_utils import File_mode, get_file


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        file: Path = get_file(working_directory, File_mode.READ, file_path)

        return get_content(file)
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"


def get_content(file_path: Path) -> str:
    with open(file_path, mode="r") as file:
        content = file.read(MAX_CHARS_TO_SEND_TO_LLM)

        # check whether one more character can be read.
        # If so, not whole contents were read.
        # Add info about truncating content
        if file.read(1):
            content += (
                f'[...File "{file_path.name}" truncated at '
                + f"{MAX_CHARS_TO_SEND_TO_LLM} characters]"
            )
        return content
