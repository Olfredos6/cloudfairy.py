import requests

AUTH_EMAIL = ""
TOKEN = ""
ZONE_ID = ""

def get_headers():
    return {
        "X-Auth-Key": TOKEN,
        "X-Auth-Email": AUTH_EMAIL, 
        "Content-Type": "application/json",
    }

def patch_dns_records(zone_id=ZONE_ID, record_id=None, payload={}):
    return requests.patch(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
        json=payload,
        headers=get_headers(),
    ).json()


print(patch_dns_records(record_id="", payload={"content": "13.246.32.197"}))
