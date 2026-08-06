import subprocess  # nosec: B404
from pathlib import Path

from utils.file_utils import File_mode, get_file

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python script provided by path to a *.py file relative to working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "required": "true",
                    "description": "Path to the *.py file, relative to working directory, to be run",
                },
                "args": {
                    "type": "list[string]",
                    "required": "false",
                    "description": "List of arguments to be provided when running the Python script",
                },
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        file: Path = get_file(
            working_directory, File_mode.EXECUTTE, file_path, (".py", "Python")
        )

        command: list[str] = ["python", str(file)]
        if args != None:
            command.extend(args)

        completed_process: subprocess.CompletedProcess = subprocess.run(  # noqa: PLW1510 # nosec: B603
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        result = ""
        if completed_process.returncode != 0:
            result += (
                f"Process exited with code {completed_process.returncode}\n"
            )
        if completed_process.stdout == "" and completed_process.stderr == "":
            result += "No output produced"
        elif completed_process.stdout != "":
            result += f"STDOUT: {completed_process.stdout}\n"
        elif completed_process.stderr != "":
            result += f"STDERR: {completed_process.stderr}\n"

        return result

    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"
