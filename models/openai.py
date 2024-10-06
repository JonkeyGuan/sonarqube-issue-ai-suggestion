import os

import requests
from utils.prompt import format_prompt, system_prompt

def request_chatgpt(prompt: str) -> str:
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.geten('OPENAI_AI_MODEL')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        "model": f"{model}",
        "messages": [
            {
                "role": "system",
                "content": system_prompt()
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    openai_url = os.getenv('OPENAI_API_URL')
    response = requests.post(f'{openai_url}/v1/chat/completions', headers=headers, json=data)
    return response.json()

def run_ai(source_code: str, change: str, sonar_msg: str) -> str:
    prompt = format_prompt(source_code, sonar_msg)
    response = request_chatgpt(prompt)
    return response['choices'][0]['message']['content']
