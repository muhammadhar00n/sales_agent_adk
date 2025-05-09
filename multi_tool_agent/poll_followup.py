# poll_followup.py
import threading
import requests
import json

API_BASE   = "http://localhost:8000"
APP_NAME   = "multi_tool_agent"
SESSION_ID = input("Enter your session_id from the Dev UI: ").strip()
USER_ID    = "user"

def send_followup():
    payload = {
        "app_name":   APP_NAME,
        "user_id":    USER_ID,
        "session_id": SESSION_ID,
        "new_message": {
            "role": "user",
            "parts": [{"text": "__followup__"}]
        }
    }
    resp = requests.post(f"{API_BASE}/run_sse", json=payload, stream=True)
    for line in resp.iter_lines():
        if not line:
            continue
        text = line.decode().lstrip("data: ")
        try:
            evt = json.loads(text)
            # Extract the concatenated text of all parts
            parts = evt.get("content", {}).get("parts", [])
            message = "".join(p.get("text", "") for p in parts).strip()
            if message:
                print(f"[Agent] {message}")
        except json.JSONDecodeError:
            continue

timer = threading.Timer(60, send_followup)
timer.start()

print("⏱ Follow-up scheduled in 60s. Reply normally in the Dev UI to cancel:")
print("   (in this script) timer.cancel()")
