from pathlib import Path


def get_directory(working_directory: str, directory: str = ".") -> Path:
    absolute_path_working_directory = Path(working_directory).resolve()
    directory_path = (absolute_path_working_directory / directory).resolve()

    # check wether directory is in working directory
    target_directory_valid = (
        directory_path == absolute_path_working_directory
        or absolute_path_working_directory in directory_path.parents
    )

    if not target_directory_valid:
        raise Exception(  # noqa: TRY002
            f'Cannot list "{directory}" '
            + "as it is outside the permitted working directory"
        )

    if not directory_path.is_dir():
        raise Exception(f'"{directory}" is not a directory')  # noqa: TRY002

    return directory_path
