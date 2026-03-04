import os
import json

from scripts.extract_demo import extract_demo_data
from scripts.extract_onboarding import extract_onboarding_data
from scripts.update_agent import update_account_data
from scripts.generate_changelog import generate_changelog
from scripts.generate_agent_spec import generate_agent_spec

DEMO_FOLDER = "transcripts/demo"
ONBOARDING_FOLDER = "transcripts/onboarding"
OUTPUT_FOLDER = "outputs/accounts"


def process_demo_calls():

    files = os.listdir(DEMO_FOLDER)

    for i, file in enumerate(files):

        account_id = f"account_{i+1:03}"
        transcript_path = os.path.join(DEMO_FOLDER, file)

        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = f.read()

        # Extract demo information
        account_data = extract_demo_data(transcript, account_id)

        save_path = os.path.join(OUTPUT_FOLDER, account_id, "v1")
        os.makedirs(save_path, exist_ok=True)

        memo_path = os.path.join(save_path, "account_memo.json")

        # Save v1 memo
        with open(memo_path, "w") as f:
            json.dump(account_data, f, indent=4)

        # Generate agent spec from memo
        agent_spec_path = os.path.join(save_path, "agent_spec.json")

        generate_agent_spec(
            memo_path,
            agent_spec_path,
            "v1"
        )

        print(f"{account_id} processed successfully")


def process_onboarding_calls():

    files = os.listdir(ONBOARDING_FOLDER)

    for i, file in enumerate(files):

        account_id = f"account_{i+1:03}"
        onboarding_path = os.path.join(ONBOARDING_FOLDER, file)

        with open(onboarding_path, "r", encoding="utf-8") as f:
            transcript = f.read()

        onboarding_data = extract_onboarding_data(transcript)

        v1_path = os.path.join(
            OUTPUT_FOLDER,
            account_id,
            "v1",
            "account_memo.json"
        )

        with open(v1_path) as f:
            v1_data = json.load(f)

        # Update account
        v2_data = update_account_data(v1_data, onboarding_data)

        save_path = os.path.join(OUTPUT_FOLDER, account_id, "v2")
        os.makedirs(save_path, exist_ok=True)

        v2_memo_path = os.path.join(save_path, "account_memo.json")

        with open(v2_memo_path, "w") as f:
            json.dump(v2_data, f, indent=4)

        # Generate changelog
        changes = generate_changelog(v1_data, v2_data)

        with open(os.path.join(save_path, "changes.md"), "w") as f:
            for change in changes:
                f.write("- " + change + "\n")

        # Generate v2 agent spec
        agent_spec_path = os.path.join(save_path, "agent_spec.json")

        generate_agent_spec(
            v2_memo_path,
            agent_spec_path,
            "v2"
        )

        print(f"{account_id} updated to v2")


if __name__ == "__main__":
    process_demo_calls()
    process_onboarding_calls()