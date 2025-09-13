import os
MAX_CHARS = 10000

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    files = os.listdir(full_path)
    result = ""

    for fil in files:
        fil_size = 0
        if os.path.isdir(f"{full_path}/{fil}"):
            result += f"- {fil}: files_size={os.path.getsize(f"{full_path}/{fil}")} bytes, is_dir=True\n"
        else: 
            fil_size = os.path.getsize(f"{full_path}/{fil}")
            result += f"- {fil}: file_size={fil_size} bytes, is_dir=False\n"

    return result


