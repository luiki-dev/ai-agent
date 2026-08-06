import argparse
import os
from argparse import Namespace

from dotenv import load_dotenv
from openai import OpenAI

from functions.call_function import available_functions, call_function
from prompts import system_prompt

# parse .env file and load them as environment variables
load_dotenv()

verbose = False


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser(description="=== AI Agent ===")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    return parser.parse_args()


def initialize_client() -> OpenAI:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")

    if api_key == "" or api_key == None:
        raise RuntimeError("API key not found/loaded!  ")

    return OpenAI(
        base_url=base_url,
        api_key=api_key,
    )


def get_response(client: OpenAI, model: str, prompt: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    if verbose:
        for message in messages:
            print(f"User prompt: {message['content']}")

    return client.chat.completions.create(
        model=model,
        messages=messages,  # type: ignore
        tools=available_functions,  # type: ignore
        temperature=0,
    )


def process_response(response) -> None:
    if response.usage != None:
        if verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print(f"LLM model: {response.model}")
    else:
        raise RuntimeError("Empty 'usage' in response!")

    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)

            if verbose:
                print(f"-> {result_message['content']}")
    else:
        print(f"Response: {response.choices[0].message.content}")


def main():
    args = parse_arguments()

    user_prompt = args.user_prompt

    global verbose
    verbose = args.verbose

    try:
        ai_model: str = str(os.environ.get("AI_MODEL"))
        client = initialize_client()

        process_response(get_response(client, ai_model, user_prompt))
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
