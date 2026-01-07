"""
Day 6: Schema Validation for AI Outputs

Goal:
-----
To demonstrate why valid JSON is not sufficient and how engineers
must enforce required keys and data types before trusting AI output.

Why This Matters:
-----------------
LLMs can return JSON that parses correctly but still violates
business or system expectations, leading to silent failures.

Validation Strategy:
--------------------
1. Parse JSON
2. Check required keys
3. Validate value types
4. Reject anything that doesn't match the schema

Schema Rules:
-------------
- language: string
- purpose: string
- benefits: list of strings

What to Observe:
----------------
- JSON can parse but still fail validation
- Clear errors are better than silent corruption
"""

from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
Return a JSON object with the following keys:
- language (string)
- purpose (string)
- benefits (list of strings)

Return ONLY JSON.
"""

def validate_schema(data: dict):
    if not isinstance(data.get("language"), str):
        raise ValueError("Invalid or missing 'language'")

    if not isinstance(data.get("purpose"), str):
        raise ValueError("Invalid or missing 'purpose'")

    benefits = data.get("benefits")
    if not isinstance(benefits, list) or not all(isinstance(b, str) for b in benefits):
        raise ValueError("Invalid or missing 'benefits' list")

MAX_RETRIES = 3

for attempt in range(1, MAX_RETRIES + 1):
    print(f"\nAttempt {attempt}")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200
    )

    raw = response.choices[0].message.content
    print("Raw output:", raw)

    try:
        parsed = json.loads(raw)
        validate_schema(parsed)
        print("\n✅ Schema validated successfully")
        print(parsed)
        break

    except (json.JSONDecodeError, ValueError) as e:
        print("❌ Validation failed:", e)

else:
    print("\n🚨 All attempts failed schema validation")
