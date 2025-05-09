# Sales Agent using Google ADK

This project implements a conversational sales agent leveraging Google’s Agent Development Kit (ADK) and AI Studio’s Gemini model. It handles multiple lead interactions concurrently, collects specific information, and follows up with unresponsive leads after a simulated delay.

## Features

- **Agent Development Kit (ADK)**: Uses `google-adk` to define and run the agent.
- **Step-by-step lead collection**: Consent → name → age → country → interest.
- **Data persistence**: Saves all lead responses to `leads.csv`.
- **Follow-up mechanism**: Simulates a 24‑hour no‑response check‑in with a 60‑second demo delay.

## Repository Structure

```
sales_agent_adk/
├── .gitignore
├── README.md             # This file
├── requirements.txt      # Python dependencies
└── multi_tool_agent/
    ├── __init__.py
    ├── agent.py          # ADK agent definition
    ├── .env              # API key & config (not committed)
    └── poll_followup.py  # Follow‑up simulator script
```

## Prerequisites

- Python 3.10+
- Git
- Google AI Studio API Key

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/sales_agent_adk.git
   cd sales_agent_adk
   ```

2. **Create & activate a virtual environment**:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```


# note api key is already defined in .env file so no need to write it again.
4. **Configure your API key**:

   ```bash
   cd multi_tool_agent
   copy NUL .env        # Windows
   touch .env           # macOS/Linux
   ```

   Open `.env` and add:

   ```dotenv
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=YOUR_API_KEY_HERE
   ```

## Running the Agent

### ADK Dev UI

1. From the project root:
   ```bash
   run this command: adk web
   ```
2. Open your browser at `http://localhost:8000`.
3. Select `multi_tool_agent` from the dropdown.
4. In the input box, type any kick‑off message (e.g. `start`) and press **Send**.
5. Follow the prompts:
   - `yes` → agent asks for name, age, country, interest.
   - `no`  → agent ends with a polite goodbye.

### Simulating Follow‑Up

To demo the no‑response follow‑up after a simulated 24 hours (60 seconds):

1. Open a new terminal (leave the Dev UI open).
2. Run:
   ```bash
   python multi_tool_agent/poll_followup.py
   ```
3. Enter the `session_id` shown in the Dev UI network logs.
4. **Do not** reply in the Dev UI. After 60 seconds, you will see:
   ```
   Just checking in to see if you’re still interested. Let me know when you're ready to continue.
   ```
   in both the poll script and the Dev UI chat.

## leads.csv

Every conversation is persisted in `multi_tool_agent/leads.csv` with columns:

```
lead_id, name, age, country, interest, status
```

- `status` is one of: `pending`, `secured`, or `no_response`.

## Creating requirements.txt

To update dependencies:

```bash
pip freeze > requirements.txt
```

## Notes

- **Do not** commit your `.env` or `.venv` to source control.
- The follow‑up mechanism uses a manual poller to simulate proactive messages in the Dev UI.

---

Happy selling! 🚀
