import os
import google.genai.types as types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the specified directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file.",
            )
        }
    )
)

def write_file(working_directory, file_path, content):
    # Check if the file path is valid and exists
    try:
        wd = os.path.realpath(os.path.abspath(working_directory))
        target = os.path.realpath(os.path.abspath(os.path.join(working_directory, file_path)))

        if os.path.commonpath([wd, target]) != wd:
            print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
            return None
        if not os.path.exists(target):
            print(f'File "{file_path}" does not exist. Creating it.')
            os.makedirs(os.path.dirname(target), exist_ok=True)

        # Write the content to the file
        with open(target, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

