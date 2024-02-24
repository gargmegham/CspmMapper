import hashlib
import hmac
import json
import time
import os
import requests

BASE_API_URL = "https://api.cloudsploit.com"
PROGRAMS = json.load(open("programs.json", "r"))["data"]
CSPM_KEY = os.getenv("CSPM_KEY")
CSPM_SECRET = os.getenv("CSPM_SECRET")


def generate_signature(secret_bytes, string_bytes):
    return hmac.new(secret_bytes, msg=string_bytes, digestmod=hashlib.sha256).hexdigest()


def generate_headers(path, api_key=None, api_secret=None, method="GET", body=""):
    timestamp = str(int(time.time() * 1000))
    string = timestamp + method + path + body
    secret_bytes = bytes(api_secret, "utf-8")
    string_bytes = bytes(string, "utf-8")
    sig = generate_signature(secret_bytes, string_bytes)
    headers = {
        "accept": "application/json",
        "x-api-key": api_key,
        "x-signature": sig,
        "x-timestamp": timestamp,
        "content-type": "application/json",
    }
    return headers


def get_latest_scan(api_key=None, api_secret=None, key_id=None):
    path = "/v2/scans"
    query_params = {"limit": 1}
    if key_id is not None:
        query_params["key_id"] = key_id
    url = f"{BASE_API_URL}{path}"
    my_headers = generate_headers(path, api_key, api_secret)
    response = requests.get(url, headers=my_headers, params=query_params)
    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])[0] if data.get("data") else {}
    else:
        return {"status": response.status_code}


def list_keys(api_key=None, api_secret=None):
    path = "/v2/keys"
    url = f"{BASE_API_URL}{path}"
    response = requests.get(url, headers=generate_headers(path, api_key, api_secret))
    if response.status_code == 200:
        data = response.json()
        return [
            {
                "id": key["id"],
                "name": key["name"],
                "cloud": key["cloud"],
            }
            for key in data.get("data", [])
        ]
    else:
        return {"status": response.status_code}


def list_programs(api_key=None, api_secret=None):
    path = "/v2/programs"
    url = f"{BASE_API_URL}{path}"
    response = requests.get(url, headers=generate_headers(path, api_key, api_secret))
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"status": response.status_code}


def get_compliance_report(scan_id, program_id=1, api_key=None, api_secret=None, summary=False):
    path = "/v2/compliances"
    query_params = {"scan_id": scan_id, "program_id": program_id}
    if summary:
        query_params["summary"] = "compliance"
    url = f"{BASE_API_URL}{path}"
    response = requests.get(url, headers=generate_headers(path, api_key, api_secret), params=query_params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": response.status_code}


if __name__ == "__main__":
    latest_scan_id = get_latest_scan(CSPM_KEY, CSPM_SECRET, "47430").get("id")

    for program in PROGRAMS:
        my_compliance_report_context = get_compliance_report(
            latest_scan_id,
            program["id"],
            CSPM_KEY,
            CSPM_SECRET,
        )
        with open(f"{program['name']}.json", "w") as f:
            json.dump(my_compliance_report_context, f)
