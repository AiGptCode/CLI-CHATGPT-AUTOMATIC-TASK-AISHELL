import os
import subprocess
import sys
import json
import atexit
from datetime import datetime

# Define constants
OPENAI_KEY = os.environ.get("OPENAI_KEY")
GPT_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.7
MAX_TOKENS = 1024
SIZE = "512x512"
CONTEXT = False
MULTI_LINE_PROMPT = False
COMMAND_GENERATION_PROMPT = "The following command will be executed:"
HISTORY_FILE = os.path.expanduser("~/.chatgpt_history")

# Function to handle errors
def handle_error(response):
    if "error" in response:
        error_type = response["error"]["type"]
        error_message = response["error"]["message"]
        print(f"Your request to OpenAI API failed: {error_type}")
        print(error_message)
        sys.exit(1)

# Function to list available models
def list_models():
    models_response = subprocess.run(
        ["curl", "https://api.openai.com/v1/models", "-sS", "-H", f"Authorization: Bearer {OPENAI_KEY}"],
        capture_output=True,
        text=True,
    ).stdout
    models_data = json.loads(models_response)["data"]
    print("This is a list of models currently available at OpenAI API:")
    for model in models_data:
        print(f"{model['id']} (Owned by: {model['owned_by']}, Created: {model['created']})")

# Function to send a request to OpenAI's completions endpoint
def request_to_completions(prompt):
    data = {
        "model": GPT_MODEL,
        "prompt": prompt,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }
    response = subprocess.run(
        ["curl", "https://api.openai.com/v1/completions", "-sS", "-H", "Content-Type: application/json", "-H", f"Authorization: Bearer {OPENAI_KEY}"],
        input=json.dumps(data),
        capture_output=True,
        text=True,
    ).stdout
    return json.loads(response)

# Function to request image generation from OpenAI
def request_to_image(prompt):
    data = {
        "prompt": prompt.split("image:")[1].strip(),
        "n": 1,
        "size": SIZE,
    }
    response = subprocess.run(
        ["curl", "https://api.openai.com/v1/images/generations", "-sS", "-H", "Content-Type: application/json", "-H", f"Authorization: Bearer {OPENAI_KEY}"],
        input=json.dumps(data),
        capture_output=True,
        text=True,
    ).stdout
    return json.loads(response)

# Function to send a request to OpenAI's chat completions endpoint
def request_to_chat(message):
    data = {
        "model": GPT_MODEL,
        "messages": message,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }
    response = subprocess.run(
        ["curl", "https://api.openai.com/v1/chat/completions", "-sS", "-H", "Content-Type: application/json", "-H", f"Authorization: Bearer {OPENAI_KEY}"],
        input=json.dumps(data),
        capture_output=True,
        text=True,
    ).stdout
    return json.loads(response)

# ... (other functions)

# Main function
def main():
    global chat_context, chat_message
    chat_context = ""
    chat_message = ""

    # Parse command-line arguments
    args = sys.argv[1:]
    while args:
        arg = args.pop(0)
        if arg in ("-l", "--list"):
            list_models()
            sys.exit(0)
        # ... (other argument handling)

    # ... (rest of your code)

if __name__ == "__main__":
    main()
