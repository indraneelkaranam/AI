from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = "Explain the importance of virtual environments in Python in 3 bullet points."

temperatures = [0.0, 0.7, 1.2]

for temp in temperatures:
    print(f"\n====== Temperature: {temp} ======")

    for run in range(1, 4):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp
        )
        print(f"\nRun {run}:")
        print(response.choices[0].message.content)
