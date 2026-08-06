from pathlib import Path

from functions.get_directory import get_directory


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
