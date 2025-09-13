import os
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    file_content_string = None
    try: 
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(full_path) > MAX_CHARS:
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return file_content_string
    except Exception as e:
        return f'Error: reading file "{file_path}": {e}'
