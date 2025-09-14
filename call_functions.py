import os
from functions.get_files_info import *
from functions.run_python_file import *
from functions.get_file_content import *
from functions.write_file import *
from google.genai import types

def call_function(function_call_part, verbose=False):
    working_directory = "calculator"
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    result = ""
    if function_call_part.name == "get_files_info":
        result = get_files_info(working_directory, **function_call_part.args)
    if function_call_part.name == "get_file_content":
        result = get_file_content(working_directory, **function_call_part.args)
    if function_call_part.name == "write_file":
        result = write_file(working_directory, **function_call_part.args)
    if function_call_part.name == "run_python_file":
        result = run_python_file(working_directory, **function_call_part.args)

    if result == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )
