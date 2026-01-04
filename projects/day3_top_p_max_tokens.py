from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = "Explain why virtual environments are important in Python using bullet points."

experiments = [
    {"top_p": 1.0, "max_tokens": 150},
    {"top_p": 0.3, "max_tokens": 150},
    {"top_p": 1.0, "max_tokens": 40},
]

for exp in experiments:
    print(f"\n==== top_p={exp['top_p']}, max_tokens={exp['max_tokens']} ====")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        top_p=exp["top_p"],
        max_tokens=exp["max_tokens"]
    )

    print(response.choices[0].message.content)
