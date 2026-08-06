from pathlib import Path

from utils.file_utils import get_directory

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        directory_path: Path = get_directory(working_directory, directory)

        return get_dir_contents_info(directory_path)
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"


def get_dir_contents_info(directory: Path) -> str:
    directory_contents: str = f"Result for '{directory.name}' directory:\n"

    for item in directory.iterdir():
        directory_contents = directory_contents + (
            f"- {item.name}: "
            + f"file_size={item.stat(follow_symlinks=False).st_size} bytes, "
            + f"is_dir={item.is_dir()}\n"
        )

    return directory_contents
