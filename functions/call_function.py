import os
import google.genai.types as types
from functions.get_files_info import *
from functions.write_file import *
from functions.run_python_file import *
from functions.get_file_content import *
from config import WORKING_DIR



def call_function(function_call_part: types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({[WORKING_DIR] + function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_dict = {
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
        "get_file_content": get_file_content
    }

    if function_call_part.name in function_dict:
        result = function_dict[function_call_part.name]([WORKING_DIR] + function_call_part.args)
    else:
        print(f" - Unknown function: {function_call_part.name}")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": result},
        )
    ],
)

