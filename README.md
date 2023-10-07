
```
# ChatGPT-OpenAI Integration

![GitHub stars](https://img.shields.io/github/stars/AiGptCode/CLI-ChatGpt-automatic-Shell)
![GitHub forks](https://img.shields.io/github/forks/AiGptCode/CLI-ChatGpt-automatic-Shell)
![GitHub license](https://img.shields.io/github/license/AiGptCode/CLI-ChatGpt-automatic-Shell)

## Overview

This repository contains a Python script that integrates OpenAI's GPT-3.5 Turbo with chat-based and completion-based functionality. You can use this script to interact with the OpenAI API for various tasks.

## Prerequisites

Before using this script, make sure you have the following prerequisites installed:

- Python 3.x
- `curl` (command-line tool)
- An OpenAI API key (set it as an environment variable `OPENAI_KEY`)

## Usage

To use this script, you can run it from the command line with different options and prompts. Here are some examples:

- List available OpenAI models:
  ```
  python script.py -l
  ```

- Perform chat-based completions:
  ```
  python script.py -c "Your chat message here."
  ```

- Perform completion-based generation:
  ```
  python script.py -g "Your generation prompt here."
  ```

- Generate images from prompts:
  ```
  python script.py -i "image: Generate a beautiful sunset."
  ```

Make sure to customize the `GPT_MODEL`, `TEMPERATURE`, `MAX_TOKENS`, and other constants according to your needs.

## Documentation

For detailed information on how to use this script and the available options, refer to the [official OpenAI API documentation](https://beta.openai.com/docs/).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT-3.5 Turbo API.

Feel free to contribute to this project or open issues if you encounter any problems or have suggestions for improvements.
```
