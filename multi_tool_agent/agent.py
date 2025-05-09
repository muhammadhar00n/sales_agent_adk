# multi_tool_agent/agent.py

import os
import csv
from google.adk.agents import Agent

# —— CSV setup ——
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "leads.csv")
FIELDNAMES = ["lead_id", "name", "age", "country", "interest", "status"]

if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

def save_lead(lead_id: str, field: str, value: str) -> dict:
    rows, found = [], False
    with open(CSV_PATH, newline="") as f:
        for r in csv.DictReader(f):
            if r["lead_id"] == lead_id:
                r[field] = value
                found = True
            rows.append(r)
    if not found:
        new = {h: "" for h in FIELDNAMES}
        new["lead_id"] = lead_id
        new[field]    = value
        new["status"] = "pending"
        rows.append(new)
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return {"status":"success"}

# —— Agent instruction ——
instruction = """
You are a friendly sales assistant.

Step 1: Greet and get consent:
  “Hey there, thank you for filling out the form. I'd like to gather some information from you. Is that okay?”

- If user replies “no”, respond:
    “Alright, no problem. Have a great day!”
  and call save_lead(lead_id, "status", "no_response") → END.

- If user replies “yes”, proceed:

Step 2: Ask:
  “What is your full name?”
  → save_lead(lead_id, "name", answer)

Step 3: Ask:
  “What is your age?”
  → save_lead(lead_id, "age", answer)

Step 4: Ask:
  “Which country are you from?”
  → save_lead(lead_id, "country", answer)

Step 5: Ask:
  “What product or service are you interested in?”
  → save_lead(lead_id, "interest", answer)

Step 6: Conclude:
  “Thanks for all the info! We’ll be in touch soon.”
  → save_lead(lead_id, "status", "secured")

Manual Follow-up:
- If you type `__followup__` at any point, reply:
    “Just checking in to see if you’re still interested.”
"""

root_agent = Agent(
    name="sales_agent",
    model="gemini-2.0-flash",
    description="Sales agent collecting leads step-by-step",
    instruction=instruction.strip(),
    tools=[save_lead],
)
