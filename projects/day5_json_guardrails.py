"""
Day 5: JSON Guardrails with Validation and Retries

Goal:
-----
To demonstrate how engineers handle unreliable LLM outputs by validating
responses and retrying instead of assuming correctness.

Why This Exists:
----------------
LLMs generate text, not guaranteed data structures. Even when asked for
JSON, outputs can break parsers. This script shows a minimal, practical
pattern to make AI outputs safer.

Strategy Used:
--------------
1. Ask the model for JSON
2. Attempt to parse using json.loads()
3. If parsing fails:
   - Retry the request (up to N times)
4. If all retries fail:
   - Exit with a controlled failure

Parameters:
-----------
temperature = 0.7
- Allows variation so retries are meaningful

max_retries = 3
- Limits runaway failures and cost

What to Observe:
----------------
- Some runs succeed on first try
- Some require retries
- Failures are now controlled, not random
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

MAX_RETRIES = 3

for attempt in range(1, MAX_RETRIES + 1):
    print(f"\nAttempt {attempt}:")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200
    )

    raw_output = response.choices[0].message.content
    print("Raw output:", raw_output)

    try:
        parsed = json.loads(raw_output)
        print("\n✅ JSON parsed successfully!")
        print(parsed)
        break

    except json.JSONDecodeError as e:
        print("❌ Parsing failed:", e)

else:
    print("\n🚨 All retries failed. Escalating failure safely.")
