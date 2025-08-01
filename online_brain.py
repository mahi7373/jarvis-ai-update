# online_brain.py
import os
from openai import OpenAI

class OnlineBrain:
    def __init__(self):
        print("☁️ Online Brain Ready (OpenAI/Groq API)...")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
