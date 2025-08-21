import os
from . import config
MAX_CHARS = config.MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # Check if the file exists and is a regular file
        wd = os.path.realpath(os.path.abspath(working_directory))
        target = os.path.realpath(os.path.abspath(os.path.join(working_directory, file_path)))
        print(f'Working directory: {wd}')
        print(f'Target file: {target}')

        if os.path.commonpath([wd, target]) != wd:
            print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
            return None

        if not os.path.isfile(target):
            print(f'Error: File not found or is not a regular file: "{file_path}"')
            return None

        # Read the file content and return it
        with open(target, "r") as f:
            content = f.read()
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS] + f"[...File '{target}' truncated at 10000 characters]"

        return content
    except Exception as e:
        print(f'Error: {e}')