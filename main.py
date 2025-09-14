import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import *
from functions.run_python_file import *
from functions.get_file_content import *
from functions.write_file import *
from prompts import *
from call_functions import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    verbose = False
    user_prompt = sys.argv[1]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(10):
        response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents = messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt,
                                           tools=[available_functions],),
        )
        if response is None or response.usage_metadata is None:
            print("response malformed")
            return
        
        tokens_p = response.usage_metadata.prompt_token_count
        tokens_r = response.usage_metadata.candidates_token_count
        functions_call_part = response.function_calls
        
        
        if len(sys.argv) == 3:
            if sys.argv[2] == "--verbose":
                verbose = True
            
        if verbose: 
            print(f"Prompt tokens: {tokens_p}")
            print(f"Response tokens: {tokens_r}")
            print(f"User prompt: {user_prompt}")

        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in functions_call_part:
                result = call_function(function_call_part, verbose)
                messages.append(result)
        else:
            print(response.text)
            return


if __name__ == "__main__":
    main()
