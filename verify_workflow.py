import requests
import json
import time

def test_workflow():
    url = "http://localhost:5000/api/workflow/run"

    payload = {
        "message": "My IndiGo flight 6E-234 from Delhi to Mumbai on 28 October 2025 was delayed by 5 hours",
        "auto_submit": False
    }

    print("Testing End-to-End Workflow...")
    print(f"Input: {payload['message']}")

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            data = response.json()
            print("\n✅ Workflow Successful!")
            print(json.dumps(data, indent=2))

            # Checks
            if data['status'] == 'success':
                print("\n[PASS] Workflow status is success")
            else:
                print(f"\n[FAIL] Workflow status is {data['status']}")

            if 'intake' in data and data['intake'].get('flight_number') == '6E-234':
                print("[PASS] Intake Agent extracted flight number")
            else:
                print("[FAIL] Intake Agent failed")

            if 'eligibility' in data and data['eligibility'].get('eligible') == True:
                print("[PASS] Eligibility Agent confirmed eligibility")
            else:
                print("[FAIL] Eligibility Agent failed")

            if 'documents' in data and data['documents'].get('success') == True:
                print("[PASS] Document Agent generated files")
                print(f"      File: {data['documents'].get('claim_letter_path')}")
            else:
                print("[FAIL] Document Agent failed")

        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"\n❌ Exception: {e}")

if __name__ == "__main__":
    time.sleep(2) # Wait for server
    test_workflow()
