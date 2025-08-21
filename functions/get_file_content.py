import os
from . import config
import google.genai.types as types
MAX_CHARS = config.MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in the specified directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be read, relative to the working directory.",
            ),
        }
    )
)

def get_file_content(working_directory, file_path):
    try:
        # Check if the file exists and is a regular file
        wd = os.path.realpath(os.path.abspath(working_directory))
        target = os.path.realpath(os.path.abspath(os.path.join(working_directory, file_path)))

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
        return f'Error: {e}'