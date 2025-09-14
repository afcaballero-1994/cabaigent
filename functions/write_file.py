import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        path_to_file = os.path.dirname(full_path)
        if not os.path.exists(path_to_file):
            os.makedirs(path_to_file)
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: writing file "{file_path}": {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file, this function can only be called to work in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="if the file does not exist it will be created, this is the file where the content will be written",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="This is the content that will be used to write to the file"
            ),
        },
    ),
)
