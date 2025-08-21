import os
import subprocess
import sys
import google.genai.types as types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to be executed, relative to the working directory.",
            ),
        }
    )
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        #Verify that the file exists and is a Python file
        wd = os.path.realpath(os.path.abspath(working_directory))
        target = os.path.realpath(os.path.abspath(os.path.join(working_directory, file_path)))

        if os.path.commonpath([wd, target]) != wd:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target):
            return f'Error: File "{file_path}" not found.'
        if not str.endswith(target, ".py"):
            return f'Error: "{file_path}" is not a Python file'

        #Execute the Python file
        executable = subprocess.run([sys.executable, target, *args], timeout=30, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = "STDOUT:" + executable.stdout.decode("utf-8")
        if executable.stderr:
            output += "\nSTDERR:" + executable.stderr.decode("utf-8")
        if executable.returncode != 0:
            return f'Process exites with code {executable.returncode}.'
        if len(output) == 0:
            return "No output produced."
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"