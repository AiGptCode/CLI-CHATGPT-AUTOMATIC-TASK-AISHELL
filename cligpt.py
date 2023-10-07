‏import subprocess
‏import os
‏import sys
‏import json
‏from datetime import datetime

# اطلاعات مربوط به تنظیمات اپلیکیشن
‏OPENAI_KEY = os.environ.get("OPENAI_KEY")
‏MODEL = "gpt-3.5-turbo"
‏TEMPERATURE = 0.7
‏MAX_TOKENS = 1024
‏SIZE = "512x512"
‏CONTEXT = False
‏MULTI_LINE_PROMPT = False

# دستورات خط فرمان ممکن
‏COMMAND_GENERATION_PROMPT = (
‏    "You are a Command Line Interface expert and your task is to provide functioning shell commands. "
‏    "Return a CLI command and nothing else - do not send it in a code block, quotes, or anything else, "
‏    "just the pure text CONTAINING ONLY THE COMMAND. If possible, return a one-line bash command or chain "
‏    "many commands together. Return ONLY the command ready to run in the terminal. The command should do the following:"
)

# تنظیم تاریخ فعلی
‏today_date = datetime.today().strftime("%m/%d/%Y")

# تابع برای ارسال درخواست به API OpenAI
‏def send_request_to_openai(prompt):
‏    cmd = [
‏        "curl",
‏        "https://api.openai.com/v1/completions",
‏        "-sS",
‏        "-H",
‏        "Content-Type: application/json",
‏        "-H",
‏        f"Authorization: Bearer {OPENAI_KEY}",
‏        "-d",
‏        json.dumps(
            {
‏                "model": MODEL,
‏                "prompt": prompt,
‏                "max_tokens": MAX_TOKENS,
‏                "temperature": TEMPERATURE,
            }
        ),
    ]
‏    response = subprocess.check_output(cmd).decode("utf-8")
‏    return response

# تابع برای اضافه کردن پاسخ دستیار به متغیر مکالمه
‏def add_assistant_response_to_chat_message(response_data):
‏    global chat_message
‏    chat_message += ', {"role": "assistant", "content": "' + response_data + '"}'

# تابع برای فراخوانی درخواست دستورات خط فرمان
‏def handle_command_generation(prompt):
‏    request_prompt = COMMAND_GENERATION_PROMPT + prompt
‏    chat_message = '{"role": "user", "content": "' + request_prompt + '"}'
‏    response = send_request_to_openai(chat_message)
‏    response_data = json.loads(response)["choices"][0]["message"]["content"]

‏    print("Processing...")
‏    print(response_data)

    # چک کردن برای دستورات خطرناک
‏    dangerous_commands = ["rm", ">", "mv", "mkfs", ":(){:|:&};", "dd", "chmod", "wget", "curl"]
‏    for command in dangerous_commands:
‏        if command in response_data:
‏            print("Warning! This command can change your file system or download external scripts & data. Please do not execute code that you don't understand completely.")

‏    run_answer = input("Would you like to execute it? (Yes/No): ")
‏    if run_answer.lower() in ["yes", "y", "ok"]:
‏        print("Executing command:", response_data)
‏        os.system(response_data)

# تابع برای تبدیل تاریخ معادل
‏def convert_date(date_str):
‏    date_obj = datetime.strptime(date_str, "%m/%d/%Y")
‏    return date_obj.strftime("%Y-%m-%d")

# تنظیم متغیرهای اولیه
‏chat_message = ""
‏prompt = ""
‏pipe_mode_prompt = ""
‏running = True
‏chat_context = ""
‏system_prompt = (
‏    "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. "
‏    "Current date: " + today_date + ". Knowledge cutoff: 9/1/2021."
)

# تایید کلید API
‏if OPENAI_KEY is None:
‏    print("You need to set your OPENAI_KEY to use this script")
‏    print("You can set it temporarily by running this on your terminal: export OPENAI_KEY=YOUR_KEY_HERE")
‏    sys.exit(1)

# تابع برای افزودن متن به متغیر مکالمه
‏def append_to_chat_history(message):
‏    global chat_message
‏    chat_message += message + "\n"

# تنظیم دستورات خط فرمان بر اساس ورودی
‏if len(sys.argv) > 1:
‏    if sys.argv[1] == "-l" or sys.argv[1] == "--list":
‏        list_models():
    with open(os.path.expanduser("~/.chatgpt_history"), "w") as history_file:
        history_file.write("")

# تنظیم حالت چت ورودی
if sys.stdin.isatty():
    print("Welcome to chatgpt. You can quit with 'exit' or 'q'.")
    if not MULTI_LINE_PROMPT:
        append_to_chat_history(input("Enter a prompt: "))
else:
    pipe_mode_prompt = sys.stdin.read()

while running:
    if not pipe_mode_prompt:
        if MULTI_LINE_PROMPT:
            print("Enter a prompt: (Press Enter then Ctrl-D to send)")
            user_input_temp_file = open("user_input_temp_file.txt", "w")
            user_input_temp_file.write(sys.stdin.read())
            user_input_temp_file.close()
            with open("user_input_temp_file.txt", "r") as file:
                input_from_temp_file = file.read()
            os.remove("user_input_temp_file.txt")
            prompt = input_from_temp_file
        else:
            print("Enter a prompt:")
            prompt = input()

    if prompt.lower() in ["exit", "q"]:
        running = False

    if prompt.startswith("image:"):
        image_prompt = prompt[len("image:") :]
        response = send_request_to_openai(image_prompt)
        image_url = json.loads(response)["data"][0]["url"]
        print(f"Your image was created.\nLink: {image_url}")

        if "TERM_PROGRAM" in os.environ:
            if os.environ["TERM_PROGRAM"] == "iTerm.app":
                subprocess.run(["curl", "-sS", image_url, "-o", "temp_image.png"])
                subprocess.run(["imgcat", "temp_image.png"])
                os.remove("temp_image.png")
            elif os.environ["TERM"] == "xterm-kitty":
                subprocess.run(["curl", "-sS", image_url, "-o", "temp_image.png"])
                subprocess.run(["kitty", "+kitten", "icat", "temp_image.png"])
                os.remove("temp_image.png")
        else:
            open_image = input("Would you like to open it? (Yes/No): ")
            if open_image.lower() in ["yes", "y", "ok"]:
                subprocess.run(["open", image_url])

    elif prompt == "history":
        with open(os.path.expanduser("~/.chatgpt_history"), "r") as history_file:
            print(history_file.read())

    elif prompt == "models":
        list_models()

    elif prompt.startswith("model:"):
        model_id = prompt[len("model:") :].strip()
        models_response = subprocess.check_output(
            ["curl", "https://api.openai.com/v1/models", "-sS", "-H", f"Authorization: Bearer {OPENAI_KEY}"]
        ).decode("utf-8")
        models_data = json.loads(models_response)["data"]
        model_info = next((model for model in models_data if model["id"] == model_id), None)
        if model_info:
            print(f"Complete details for model: {model_id}\n{model_info}")
        else:
            print(f"Model {model_id} not found.")

    elif prompt.startswith("command:"):
        command_prompt = prompt[len("command:") :].strip()
        handle_command_generation(command_prompt)

    elif MODEL.startswith("gpt-"):
        response = send_request_to_openai(prompt)
        response_data = json.loads(response)["choices"][0]["message"]["content"]

        print("Processing...")
        print(response_data)

        add_assistant_response_to_chat_message(response_data)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        append_to_chat_history(f"{timestamp} {prompt}\n{response_data}")

    else:
        response = send_request_to_openai(prompt)
        response_data = json.loads(response)["choices"][0]["text"]

        print("Processing...")
        print(response_data)

        if CONTEXT:
            chat_context += f"\nQ: {prompt}"
            while len(chat_context.split()) * 1.3 > (MAX_TOKENS - 100):
                chat_context = chat_context[chat_context.find("\n") + 1 :]
                chat_context = f"{system_prompt}\n{chat_context}"
        response_data = response_data[2:]  # Remove 'A: ' prefix
        print(response_data)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        append_to_chat_history(f"{timestamp} {prompt}\n{response_data}")

        if CONTEXT:
            chat_context += f"\nA: {response_data}"
            while len(chat_context.split()) * 1.3 > (MAX_TOKENS - 100):
                chat_context = chat_context[chat_context.find("\n") + 1 :]
                chat_context = f"{system_prompt}\n{chat_context}"

sys.exit(0)
