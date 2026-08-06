from pathlib import Path


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path_working_directory = Path(working_directory).resolve()
        directory_path = (absolute_path_working_directory / directory).resolve()

        # check wether directory is in working directory
        target_directory_valid = (
            directory_path == absolute_path_working_directory
            or absolute_path_working_directory in directory_path.parents
        )

        if not target_directory_valid:
            return (
                f'Error: Cannot list "{directory}" '
                + "as it is outside the permitted working directory"
            )

        if not directory_path.is_dir():
            return f'Error: "{directory}" is not a directory'

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
