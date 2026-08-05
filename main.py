import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")
base_url = os.environ.get("OPENAI_BASE_URL")

if api_key == "" or api_key == None:
    raise RuntimeError("API key not found/loaded!  ")


client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)


def main():
    print("Hello from ai-agent!")

    ai_model: str = str(os.environ.get("AI_MODEL"))
    messages = [
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ]
    response = client.chat.completions.create(model=ai_model, messages=messages)  # type: ignore

    print(f"Response: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
