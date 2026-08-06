import json
from collections.abc import Callable

from config import WORKING_DIRECTORY
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = [
    schema_get_file_content,
    schema_get_files_info,
    schema_write_file,
    schema_run_python_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")
    tool_call_id = tool_call.id

    function_args["working_directory"] = WORKING_DIRECTORY

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_to_call = function_map[function_name]
    if function_to_call:
        try:
            result = function_to_call(**function_args)
            return get_function_result_response(tool_call_id, result)
        except Exception as e:  # noqa: BLE001
            return get_call_error_response(tool_call, function_name, e)

    else:
        return get_function_not_found_response(tool_call_id, function_name)


def get_function_not_found_response(
    tool_call_id: str, function_name: str
) -> dict[str, str]:
    return get_function_result_response(
        tool_call_id, f"Error: Unknown function: {function_name}"
    )


def get_call_error_response(
    tool_call_id: str, function_name: str, exception: Exception
) -> dict[str, str]:
    return get_function_result_response(
        tool_call_id,
        f"Error: Exception during '{function_name}' call: {exception}",
    )


def get_function_result_response(
    tool_call_id: str, content: str
) -> dict[str, str]:
    return {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": content,
    }
