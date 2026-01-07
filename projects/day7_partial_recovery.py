"""
Day 7: Partial Recovery of AI Outputs

Goal:
-----
To demonstrate how production-grade AI systems recover usable data
from imperfect model outputs instead of retrying everything.

Why This Matters:
-----------------
LLM outputs often contain a mix of:
- Correct fields
- Incorrect fields
- Missing fields

Blind retries:
- Increase cost
- Increase latency
- Increase unpredictability

Partial recovery:
- Salvages valid data
- Repairs invalid fields
- Retries only as a last resort

Recovery Strategy:
------------------
1. Parse JSON
2. Validate each field independently
3. Keep valid fields
4. Repair or default invalid ones
5. Return a safe, normalized structure

Schema:
-------
- language: string (required)
- purpose: string (required)
- benefits: list of strings (optional, recoverable)

What to Observe:
----------------
- Outputs can be "partially right"
- Intelligent recovery reduces retries
"""

from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
Return a JSON object with:
- language (string)
- purpose (string)
- benefits (list of strings)

Return ONLY JSON.
"""

def normalize_output(data: dict):
    normalized = {}

    # Required fields
    if isinstance(data.get("language"), str):
        normalized["language"] = data["language"]
    else:
        raise ValueError("language missing or invalid")

    if isinstance(data.get("purpose"), str):
        normalized["purpose"] = data["purpose"]
    else:
        raise ValueError("purpose missing or invalid")

    # Optional / recoverable field
    benefits = data.get("benefits")
    if isinstance(benefits, list):
        normalized["benefits"] = [b for b in benefits if isinstance(b, str)]
    else:
        normalized["benefits"] = []

    return normalized

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
        safe_output = normalize_output(parsed)
        print("\n✅ Recovered and normalized output:")
        print(safe_output)
        break

    except (json.JSONDecodeError, ValueError) as e:
        print("❌ Recovery failed:", e)

else:
    print("\n🚨 All attempts failed. Escalating safely.")
