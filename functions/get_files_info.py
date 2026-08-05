import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path_working_directory = os.path.abspath(working_directory)
        target_directory_path = os.path.normpath(
            os.path.join(absolute_path_working_directory, directory)
        )

        target_directory_valid = (
            os.path.commonpath(
                [absolute_path_working_directory, target_directory_path]
            )
            == absolute_path_working_directory
        )

        if not target_directory_valid:
            return f'Error: Cannot list "{directory}"'
            "as it is outside the permitted working directory"

        if not os.path.isdir(target_directory_path):
            return f'Error: "{directory}" is not a directory'

        return f'Success: "{directory}" is within the working directory'
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"
