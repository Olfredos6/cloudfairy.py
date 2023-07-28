import requests
from os import environ
from sys import argv
import json


AUTH_EMAIL = environ.get("CLOUDFLARE_AUTH_EMAIL")
KEY = environ.get("CLOUDFLARE_AUTH_KEY")
ZONE_ID = environ.get("CLOUDFLARE_ZONE_ID")

def get_headers():
    return {
        "X-Auth-Key": KEY,
        "X-Auth-Email": AUTH_EMAIL, 
        "Content-Type": "application/json",
    }

def patch_dns_records(zone_id=ZONE_ID, record_id=None, payload={}):
    response = requests.patch(
        f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
        json=payload,
        headers=get_headers(),
    ).json()
    print("updating with payload ->>", payload)
    print(response)
    if response.get("success"):
        return "CloudFlare record updated successfully."
    
    message = ""
    for error in response.get("errors"):
        message += f"Error code {error.get('code')}: {error.get('message')}"
    
    return message

print(patch_dns_records(record_id=argv[1], payload=json.loads(argv[2])))
