import os
import json
import requests
import datetime

def send_log_to_loganalytics(log_type, log_data):
    endpoint = os.environ.get('LOGS_INGESTION_ENDPOINT')
    dcr_id = os.environ.get('LOGS_INGESTION_DCR_ID')
    token = os.environ.get('LOGS_INGESTION_TOKEN')

    if not endpoint or not dcr_id or not token:
        print("❌ Missing LOGS_INGESTION_ENDPOINT, LOGS_INGESTION_DCR_ID or LOGS_INGESTION_TOKEN environment variables.")
        return

    # Each log type has its own stream in the Data Collection Rule, e.g. SmokeTestResults -> Custom-SmokeTestResults_CL
    stream = f'Custom-{log_type}_CL'
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    records = [{'TimeGenerated': timestamp, **entry} for entry in log_data]

    uri = f'{endpoint.rstrip("/")}/dataCollectionRules/{dcr_id}/streams/{stream}?api-version=2023-01-01'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    print(f"Sending to Log Analytics: {len(records)} entries")
    print(f"POST {uri}")

    response = requests.post(uri, data=json.dumps(records), headers=headers)

    print(f"Response: {response.status_code} - {response.text}")

    if response.status_code != 204:
        print(f"❌ Failed to send logs: {response.status_code} - {response.text}")
    else:
        print("✅ Logs sent to Log Analytics.")
