import os

import google.generativeai as genai
from utils.prompt import format_prompt, system_prompt

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel(os.getenv('GEMINI_AI_MODEL'))

def run_ai(source_code: str, change: str, sonar_msg: str) -> str:
    prompt = format_prompt(source_code, change, sonar_msg)
    response = model.generate_content(system_prompt() + prompt)
    return response.text
