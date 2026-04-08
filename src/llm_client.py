import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class NvidiaLLM:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY")
        )
        self.model = "meta/llama-3.1-8b-instruct"  # or your preferred model
    
    def generate_response(self, prompt, max_tokens=1000):
        """Generate response from NVIDIA LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"