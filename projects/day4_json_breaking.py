"""
Day 4: Structured Outputs and JSON Reliability

Goal:
-----
To understand how unreliable LLM outputs can be when asked to return
strictly formatted JSON, and why engineers must always validate outputs
instead of trusting prompts.

Why This Experiment Exists:
---------------------------
LLMs often *sound* confident, even when they return invalid JSON.
In real systems, this can silently break downstream services.

Parameters Used:
----------------
temperature = 0.7
- Allows some natural variation so we can observe failure cases.

top_p = 1.0
- Left at default to avoid masking structural issues.

max_tokens = 200
- High enough to prevent truncation so failures are structural, not length-based.

What to Observe:
----------------
- JSON that looks correct but fails parsing
- Missing quotes, trailing commas, extra text
- Why `json.loads()` is your first line of defense
"""

from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
Return a JSON object with the following keys:
- language
- purpose
- benefits (as a list)

Do NOT include any explanation or extra text.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=200
)

raw_output = response.choices[0].message.content

print("Raw model output:")
print(raw_output)

print("\nAttempting to parse JSON...\n")

try:
    parsed = json.loads(raw_output)
    print("Parsed JSON successfully:")
    print(parsed)
except json.JSONDecodeError as e:
    print("JSON parsing failed!")
    print("Error:", e)
