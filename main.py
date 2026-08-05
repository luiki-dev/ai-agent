import argparse
import os
from argparse import Namespace

from dotenv import load_dotenv
from openai import OpenAI

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
        {
            "role": "user",
            "content": prompt,
        }
    ]

    if verbose:
        print(f"User prompt: {messages[0]['content']}")
    return client.chat.completions.create(model=model, messages=messages)  # type: ignore


def process_response(response) -> None:
    if response.usage != None:
        if verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        raise RuntimeError("Empty 'usage' in response!")

    print(f"Response: {response.choices[0].message.content}")


def main():
    args = parse_arguments()

    user_prompt = args.user_prompt

    global verbose
    verbose = args.verbose

    ai_model: str = str(os.environ.get("AI_MODEL"))
    client = initialize_client()

    process_response(get_response(client, ai_model, user_prompt))


if __name__ == "__main__":
    main()
