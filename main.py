import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    verbose = False
    user_prompt = sys.argv[1]
    if len(sys.argv) == 3:
        if sys.argv[2] == "--verbose":
            verbose = True
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents = messages
    )
    tokens_p = response.usage_metadata.prompt_token_count
    tokens_r = response.usage_metadata.candidates_token_count
    if verbose: 
        print(f"Prompt tokens: {tokens_p}")
        print(f"Response tokens: {tokens_r}")
        print(f"User prompt: {user_prompt}")
    print(response.text)


if __name__ == "__main__":
    main()
