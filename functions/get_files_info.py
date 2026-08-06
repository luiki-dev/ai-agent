from pathlib import Path


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path_working_directory = Path(working_directory).resolve()
        target_directory_path = (
            absolute_path_working_directory / directory
        ).resolve()

        # check wether directory is in working directory
        target_directory_valid = (
            target_directory_path == absolute_path_working_directory
            or absolute_path_working_directory in target_directory_path.parents
        )

        if not target_directory_valid:
            return f'Error: Cannot list "{directory}"'
            "as it is outside the permitted working directory"

        if not target_directory_path.is_dir():
            return f'Error: "{directory}" is not a directory'

        return f'Success: "{directory}" is within the working directory'
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"
