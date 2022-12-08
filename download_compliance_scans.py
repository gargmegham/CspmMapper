import hashlib
import hmac
import json
import time

import requests

BASE_API_URL = "https://api.cloudsploit.com"
PROGRAMS = json.load(open("programs.json", "r"))["data"]
GCP_KEY = ""
CSPM_KEY = "jSQhyiWLNBKiEZqoUq4lK3"
CSPM_SECRET = "V6CmIMHUm9Z2fc0ROm9APQW9X4as4rLHOsQ"


def headers(
    path: str,
    api_key: str = None,
    api_secret: str = None,
    method: str = "GET",
    body: str = "",
) -> dict:
    timestamp = str(int(time.time() * 1000))
    string = timestamp + method + path + body
    secret_bytes = bytes(api_secret, "utf-8")
    string_bytes = bytes(string, "utf-8")
    sig = hmac.new(secret_bytes, msg=string_bytes, digestmod=hashlib.sha256).hexdigest()
    headers = {
        "accept": "application/json",
        "x-api-key": api_key,
        "x-signature": sig,
        "x-timestamp": timestamp,
        "content-type": "application/json",
    }
    return headers

def latest_scan(
    api_key: str = None, api_secret: str = None, key_id: int = None
) -> dict:
    """
    Get latest scan id
    Reference: https://cloudsploit.docs.apiary.io/#reference/scans/scans-collection/get-list-all-scans
    """
    path = f"/v2/scans"
    if key_id == None:
        url = f"{BASE_API_URL}{path}?limit=1"
    else:
        url = f"{BASE_API_URL}{path}?limit=1&key_id={key_id}"
    my_headers = headers(path, api_key, api_secret)
    response = requests.get(url, headers=my_headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data["data"][0]
    else:
        return {"status": response.status_code}

def list_keys(api_key: str = None, api_secret: str = None) -> list | dict:
    """
    List all cloud accounts (keys)
    """

    path = "/v2/keys"
    url = f"{BASE_API_URL}{path}"
    keys = []
    response = requests.get(url, headers=headers(path, api_key, api_secret))
    if response.status_code == 200:
        data = json.loads(response.text)
        for key in data["data"]:
            keys.append(
                {
                    "id": key["id"],
                    "name": key["name"],
                    "cloud": key["cloud"],
                }
            )
        return keys
    else:
        return {"status": response.status_code}

def list_programs(api_key: str = None, api_secret: str = None) -> list | dict:

    path = "/v2/programs"
    url = f"{BASE_API_URL}{path}"
    keys = []
    response = requests.get(url, headers=headers(path, api_key, api_secret))
    if response.status_code == 200:
        data = json.loads(response.text)
        json.dump(data, open("ass.json", "w"))
        print(data)
        return keys
    else:
        return {"status": response.status_code}

def compliance_report(
    scan_id: int,
    program_id: int = 1,
    api_key: str = None,
    api_secret: str = None,
    summary: bool = False,
):
    """
    Get compliance report for a compliance program

    Reference: https://cloudsploit.docs.apiary.io/#reference/compliances/compliances-collection/get-list-all-compliances
    """
    path = f"/v2/compliances"
    url = f"{BASE_API_URL}{path}?scan_id={scan_id}&program_id={program_id}"
    if summary:
        url += "&summary=compliance"
    response = requests.get(url, headers=headers(path, api_key, api_secret))
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        return {"status": response.status_code}


if __name__ == "__main__":
    latest_scan_id = latest_scan(
        CSPM_KEY,
        CSPM_SECRET,
        "47430",
    )["id"]

    for program in PROGRAMS:
        my_compliance_report_context = compliance_report(
            latest_scan_id,
            program["id"],
            CSPM_KEY,
            CSPM_SECRET,
        )
        json.dump(my_compliance_report_context, open(f"{program['name']}.json", "w"))
