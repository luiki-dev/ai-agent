from enum import Enum
from pathlib import Path


class File_mode(Enum):
    READ = "read"
    WRITE = "write"


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


def get_file(working_directory: str, mode: File_mode, file: str = ".") -> Path:
    absolute_path_working_directory = Path(working_directory).resolve()
    file_path = (absolute_path_working_directory / file).resolve()

    # check wether directory is in working directory
    target_file_valid = (
        file_path == absolute_path_working_directory
        or absolute_path_working_directory in file_path.parents
    )

    if not target_file_valid:
        raise Exception(  # noqa: TRY002
            f'Cannot {mode.value} "{file}" '
            + "as it is outside the permitted working directory"
        )

    if not file_path.is_file():
        match mode:
            case File_mode.READ:
                raise Exception(  # noqa: TRY002
                    f'File not found or is not a regular file: "{file}"'
                )
            case File_mode.WRITE:
                if file_path.is_dir():
                    raise Exception(  # noqa: TRY002
                        f'Cannot write to "{file}" as it is a directory'
                    )
                file_path.parent.mkdir(parents=True, exist_ok=True)

    return file_path


def write_file(file_path: Path, content: str) -> None:
    with open(file_path, mode="w") as file:
        file.write(content)
