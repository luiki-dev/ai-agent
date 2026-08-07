import argparse
import os
import sys
from argparse import Namespace

from dotenv import load_dotenv
from openai import OpenAI

from functions import call_function
from functions.call_function import available_functions
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


def get_response(client: OpenAI, model: str, messages) -> str:
    return client.chat.completions.create(
        model=model,
        messages=messages,  # type: ignore
        tools=available_functions,  # type: ignore
        temperature=0,
    )


def process_response(response) -> tuple[list[object], bool]:
    if response.usage != None:
        if verbose:
            print(f"###>>> Prompt tokens: {response.usage.prompt_tokens}")
            print(f"###>>> Response tokens: {response.usage.completion_tokens}")
            print(f"###>>> LLM model: {response.model}")
    else:
        raise RuntimeError("Empty 'usage' in response!")

    message = response.choices[0].message
    result_messages = []
    result_messages.append(message)

    end_conversation = False
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)  # type: ignore
            result_messages.append(result_message)
            end_conversation = False

            if verbose:
                print(f"###>>> -> {result_message['content']}")
    else:
        print(f"###>>> RESPONSE: {response.choices[0].message.content}")
        end_conversation = True

    return result_messages, end_conversation


def main():
    args = parse_arguments()

    user_prompt = args.user_prompt

    global verbose
    verbose = args.verbose

    ai_model: str = str(os.environ.get("AI_MODEL"))
    client = initialize_client()

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        if verbose:
            print(f"###>>> User PROMPT: {user_prompt}")

        finished_conversation = False

        # limited conversation loop
        for _ in range(20):
            result_messages, end_conversation = process_response(
                get_response(client, ai_model, messages)
            )

            if end_conversation:
                finished_conversation = True
                break

            for result_message in result_messages:
                messages.append(result_message)  # noqa: PERF402

        if not finished_conversation:
            print("###>>> EXCEEDED CONVERSATION LIMIT. TERMINATING!")
            sys.exit(1)

    except Exception as e:  # noqa: BLE001
        print(f"###>>> MAIN ERROR: {e}")


if __name__ == "__main__":
    main()
