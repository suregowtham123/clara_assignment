import json
import os


def generate_agent_spec(account_memo_path, output_path, version="v1"):

    with open(account_memo_path, "r") as f:
        memo = json.load(f)

    company_name = memo.get("company_name", "the company")
    business_hours = memo.get("business_hours", "unknown hours")
    emergency_rules = memo.get("emergency_routing_rules", "")
    transfer_rules = memo.get("call_transfer_rules", "")

    system_prompt = f"""
You are Clara, an AI receptionist for {company_name}.

Your job is to answer incoming calls and help customers.

BUSINESS HOURS FLOW:
1. Greet the caller politely.
2. Ask the purpose of the call.
3. Collect caller name and phone number.
4. Determine if the issue is emergency or non-emergency.
5. Route or transfer calls according to rules.
6. If transfer fails, apologize and assure follow-up.
7. Ask if they need anything else.
8. Close the call politely.

AFTER HOURS FLOW:
1. Greet caller and explain office is closed.
2. Ask for purpose of call.
3. Confirm if issue is emergency.
4. If emergency: collect name, number, and address immediately.
5. Attempt transfer according to emergency routing rules.
6. If transfer fails: apologize and promise follow-up next business day.
7. If non-emergency: collect details and confirm follow-up during business hours.
8. Ask if they need anything else before closing.

IMPORTANT RULES:
- Business hours: {business_hours}
- Emergency routing: {emergency_rules}
- Call transfer rule: {transfer_rules}

Never mention system tools or internal processes to the caller.
Only ask necessary questions to route the call.
"""

    agent_spec = {
        "agent_name": f"{company_name} AI Receptionist",
        "voice_style": "professional, calm, helpful",
        "version": version,
        "system_prompt": system_prompt.strip(),

        "key_variables": {
            "company_name": company_name,
            "business_hours": business_hours,
            "emergency_routing_rules": emergency_rules
        },

        "call_transfer_protocol": transfer_rules,

        "fallback_protocol": (
            "If transfer fails after a reasonable time, apologize to the caller "
            "and assure that the team will follow up shortly."
        )
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(agent_spec, f, indent=4)

    print("Agent spec generated:", output_path)