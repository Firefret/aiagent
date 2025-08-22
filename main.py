import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.call_function import call_function

if len(sys.argv)>3:
    print("Too many arguments")
    exit(1)
load_dotenv()

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan according to the provided function schema. You can perform the following operations:

- List files and directories
- Write content to a file
- Read content from a file
- Run a Python script

If you lack some information that is required for fulfilling the request, check what tools and functions you have available and use them, instead of asking the user for it.
If the file name wasn't provided, use get_files_info and infer the file name the user means.
If you need to read a file, use get_file_content.
If you need to write a file, use write_file.
If you need to run a Python script, use run_python_file.
While calling those functions, adhere to the provided schema and infer the values you need to provide to the functions. Don't use any other tools or functions. 
When providing file address to the functions, use the file structure of the working directory you got from get_files_info call.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
#Set variables for LLM
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file
    ]
)
if '--verbose' in sys.argv:
    verbose = True
else:
    verbose = False
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

#LLM loop
for i in range(20):
    try:
        response = client.models.generate_content(model ="gemini-2.0-flash-001", contents = messages,
                                                  config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))
        for candidate in response.candidates:
            messages.append(candidate.content)
            print(candidate.content.parts[0].text)
        #If there are function calls, call them and add the responses to the messages
        if response.function_calls:
            print("Function calls detected:")
            for function_call in response.function_calls:
                function_response = call_function(function_call, verbose)
                if not function_response.parts[0].function_response.response:
                    raise Exception(f"Error: {function_response.parts[0].function_response.response}")
                else:
                    print(f"Response: {function_response.parts[0].function_response.response}")
                    messages.append(types.Content(role="user", parts=[types.Part(text=function_response.parts[0].function_response.response["result"])]))
        elif response.text:
            print("Response text detected")
            print(response.text)
            break
    except Exception as e:
        print(f"Error: {e}")
        break

# print(response.text)
# if len(response.function_calls) > 0:
#     for function_call in response.function_calls:
#         print(f"Calling function: {function_call.name}({function_call.args})")
#         function_response = call_function(function_call)
#         if not function_response.parts[0].function_response.response:
#             raise Exception(f"Error: {function_response.parts[0].function_response.response}")
#         elif verbose:
#             print(f"-> {function_response.parts[0].function_response.response}")


if verbose:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")