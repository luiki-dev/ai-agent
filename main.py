import argparse
import os
from argparse import Namespace

from dotenv import load_dotenv
from openai import OpenAI

# parse .env file and load them as environment variables
load_dotenv()


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser(description="=== AI Agent ===")
    parser.add_argument("user_prompt", type=str, help="User prompt")
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


def main():
    print("Hello from ai-agent!")

    args = parse_arguments()

    user_prompt = args.user_prompt

    ai_model: str = str(os.environ.get("AI_MODEL"))
    client = initialize_client()

    messages = [
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    print(f"User prompt: {messages[0]['content']}")
    response = client.chat.completions.create(model=ai_model, messages=messages)  # type: ignore

    if response.usage != None:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        raise RuntimeError("Empty 'usage' in response!")

    print(f"Response: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
