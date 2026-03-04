import re

def extract_onboarding_data(transcript):

    text = transcript.lower()

    business_hours = ""
    special_customer = ""

    # Business hours
    hours_match = re.search(r'monday.*friday.*\d', text)
    if hours_match:
        business_hours = hours_match.group(0)

    # Detect special customer
    if "g&m pressure" in text or "gnm pressure" in text:
        special_customer = "G&M Pressure Washing"

    onboarding_data = {
        "business_hours": business_hours,
        "emergency_definition": [],
        "emergency_routing_rules": f"Transfer calls from {special_customer} to Ben" if special_customer else "",
        "non_emergency_routing_rules": "Collect caller details and schedule follow-up",
        "call_transfer_rules": "Transfer to Ben if caller insists",
    }

    return onboarding_data