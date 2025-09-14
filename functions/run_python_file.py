import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Will run a python script in the working directory and can only run scripts in this directory, can only be used with files that ends with the .py extension, accept the file name and the args to be passed to the script",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="this file needs to exist and have a .py extension, is the script that will be excecuted",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="this is an array of strings that are the arguments to be passed to the python script, these are optional"
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command_result = None
        if not args:   
            command_result = subprocess.run(["python3", full_path], timeout=30, capture_output=True )
        else:
            command_result = subprocess.run(["python3", full_path, "".join(args)], timeout=30, capture_output=True )
        rstdout = ""
        rstderr = ""
        rreturncode = ""
        
        if command_result == None:
            return "No output produced"
        if command_result.returncode != 0:
            rreturncode = f"Process exited with code {command_result.returncode}"
        if command_result.stdout != None:
            rstdout = f"STDOUT: {command_result.stdout.decode()}"
        if command_result.stderr != None:
            rstderr = f"STDERR: {command_result.stderr.decode()}"

        return rstdout + rstderr + rreturncode

    except Exception as e:
        return f"Error: executing Python file: {e}"
