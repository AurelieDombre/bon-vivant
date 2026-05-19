import os

def load_prompt(prompt_filename: str) -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', prompt_filename)
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()