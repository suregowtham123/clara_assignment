from groq import Groq
import json

client = Groq(api_key="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")




def chunk_text(text, size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size):
        chunks.append(" ".join(words[i:i + size]))

    return chunks

def clean_output(data):

    # remove character-level garbage
    data["emergency_definition"] = [
        x for x in data.get("emergency_definition", [])
        if isinstance(x, str) and len(x) > 3
    ]

    # remove duplicates
    data["services_supported"] = list(set(data.get("services_supported", [])))

    # remove obviously wrong services
    noise_words = [
        "email", "texts", "accounting", "customer service",
        "AI agents", "reviews", "notifications"
    ]

    data["services_supported"] = [
        s for s in data["services_supported"]
        if not any(n.lower() in s.lower() for n in noise_words)
    ]

    return data


def extract_demo_data(transcript, account_id):

    chunks = chunk_text(transcript)

    final_data = {
        "company_name": "",
        "business_hours": "",
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": "",
        "non_emergency_routing_rules": "",
        "call_transfer_rules": ""
    }

    

    for chunk in chunks:
        print("Processing chunk...")

        prompt = f"""
Extract structured business information from this call transcript.

Return ONLY JSON in this format:

{{
 "company_name": "",
 "business_hours": "",
 "services_supported": [],
 "emergency_definition": [],
 "emergency_routing_rules": "",
 "non_emergency_routing_rules": "",
 "call_transfer_rules": ""
}}

Transcript:
{chunk}
"""

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        response = completion.choices[0].message.content

        try:
            start = response.find("{")
            end = response.rfind("}") + 1

            data = json.loads(response[start:end])

            if data.get("company_name"):
                final_data["company_name"] = data["company_name"]

            if data.get("business_hours"):
                final_data["business_hours"] = data["business_hours"]

            final_data["services_supported"] += data.get("services_supported", [])
            final_data["emergency_definition"] += data.get("emergency_definition", [])

            if data.get("emergency_routing_rules"):
                final_data["emergency_routing_rules"] = data["emergency_routing_rules"]

            if data.get("non_emergency_routing_rules"):
                final_data["non_emergency_routing_rules"] = data["non_emergency_routing_rules"]

            if data.get("call_transfer_rules"):
                final_data["call_transfer_rules"] = data["call_transfer_rules"]

        except:
            print("Parsing failed for chunk")

    final_data["services_supported"] = list(set(final_data["services_supported"]))
    final_data = clean_output(final_data)
    account_data = {
        "account_id": account_id,
        "company_name": final_data["company_name"],
        "office_address": "",
        "business_hours": final_data["business_hours"],
        "services_supported": final_data["services_supported"],
        "emergency_definition": final_data["emergency_definition"],
        "emergency_routing_rules": final_data["emergency_routing_rules"],
        "non_emergency_routing_rules": final_data["non_emergency_routing_rules"],
        "call_transfer_rules": final_data["call_transfer_rules"],
        "integration_constraints": "",
        "after_hours_flow_summary": "",
        "office_hours_flow_summary": "",
        "questions_or_unknowns": [],
        "notes": "Generated using Groq LLM"
    }
    

    return account_data