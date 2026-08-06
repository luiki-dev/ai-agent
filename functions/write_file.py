from pathlib import Path

import utils.file_utils
from utils.file_utils import File_mode, get_file


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        file: Path = get_file(working_directory, File_mode.WRITE, file_path)

        utils.file_utils.write_file(file, content)

        return (
            f'Successfully wrote to "{file_path}" '
            + f"({len(content)} characters written)"
        )
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"
