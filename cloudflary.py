"""A simple CLI for interacting with the CloudFlare API.
Author: Nehemie "Alfred" Balukidi
GitHub: https://github.com/Olfredos6/cloudflary.py
Contact: @olfredos6 on Twitter and GitHub
"""
import argparse
import json
from os import environ
from sys import argv

import requests

# Email you use to log into your Cloudflare account(https://dash.cloudflare.com/profile)
AUTH_EMAIL = environ.get("CLOUDFLARE_AUTH_EMAIL")
# Your Cloudflare Global API Key (https://dash.cloudflare.com/profile/api-tokens)
KEY = environ.get("CLOUDFLARE_AUTH_KEY")
# The zone you wish to interact with (See all your zones at https://dash.cloudflare.com/)
ZONE_ID = environ.get("CLOUDFLARE_ZONE_ID")

# Default API endpoint for working with DNS Records
CLOUDFLARE_DNS_ENDPOINT = (
    f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
)


# Build headers used for each request
def get_headers():
    return {
        "X-Auth-Key": KEY,
        "X-Auth-Email": AUTH_EMAIL,
        "Content-Type": "application/json",
    }


def list_zone_records():
    """List all records on the specified zone(See ZONE_ID)."""
    response = requests.get(
        CLOUDFLARE_DNS_ENDPOINT,
        headers=get_headers(),
    ).json()

    if response.get("success"):
        return response

    message = ""
    for error in response.get("errors"):
        message += f"Error code {error.get('code')}: {error.get('message')}"

    return message


def patch_dns_records(record_id, payload):
    """Patch/Update a DNS record. This can be any value on the DNS record.
    Note: Use the `get` command to view available updatable values.

    Args:
        record_id: unique identifier of the record to be updated. This is the
                    id key returned in a successful response from the `list` command.
        payload: A dictionary containing keys to be updated and their values.
    """
    response = requests.patch(
        f"{CLOUDFLARE_DNS_ENDPOINT}/{record_id}",
        json=payload,
        headers=get_headers(),
    ).json()

    if response.get("success"):
        return "CloudFlare record updated successfully"

    message = ""
    for error in response.get("errors"):
        message += f"Error code {error.get('code')}: {error.get('message')}"

    return message


def get_dns_record(record_id, key=None):
    """Get details of a DNS record.

    Args:
        record_id: unique identifier of the record to be updated.
        key: filters the returned JSON text to only the specified key.
            Defaults to None.
    """
    response = requests.get(
        f"{CLOUDFLARE_DNS_ENDPOINT}/{record_id}",
        headers=get_headers(),
    ).json()

    if response.get("success"):
        return response.get("result") if not key else response.get("result").get(key)

    message = ""
    for error in response.get("errors"):
        message += f"Error code {error.get('code')}: {error.get('message')}"

    return message


def main():
    parser = argparse.ArgumentParser(description="Manage Cloudflare DNS records")
    parser.add_argument(
        "action", choices=["list", "update", "get"], help="Action to perform"
    )

    if len(argv) > 1 and argv[1] in ["update", "get"]:
        parser.add_argument(
            "--record-id", required=True, help="Cloudflare DNS record ID"
        )
        if argv[1] == "get":
            parser.add_argument(
                "--key", required=False, help="Key in a DNS record dictionary"
            )

    if len(argv) > 1 and argv[1] == "update":
        parser.add_argument("--payload", required=True, help="JSON payload for update")

    args = parser.parse_args()

    if args.action == "list":
        result = list_zone_records()
        print(json.dumps(result, indent=2))
    elif args.action == "update":
        payload = json.loads(args.payload)
        result = patch_dns_records(record_id=args.record_id, payload=payload)
        print(result)
    elif args.action == "get":
        print(dir(args))
        result = get_dns_record(record_id=args.record_id, key=args.key)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
