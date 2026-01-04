from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = "Explain why virtual environments are important in Python."

for i in range(3):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    print(f"\n--- Run {i+1} ---")
    print(response.choices[0].message.content)
