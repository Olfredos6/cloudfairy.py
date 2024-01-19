
# A CLI for viewing and editing Cloudflare DNS records.

If you are using Cloudflare as your CDN or proxy to a server with no reserved IP address from a cloud provider, you could use this command line utility script to update your records as desired. Most often, you would want to update your Cloudflare records when the server is switched on, with the newly attributed IP address, without having to connect to Cloudflare(manually). This tool offers an `update` command that allows doing just that.

Say you have the following records on Cloudflare:
![Alt text](image.png)

The `test` server is frequently switched on and off and its IP address changes every time it is started. Running this utility by passing it a `--record-id` argument of the target record and a `--payload` containing a JSON string of the properties and values of the record to update will apply the change to your record.

## How to use it

### Prerequisites

- Make sure you have `wget` or similar tool installed on your machine
- Have Python 3 installed
- Add your Cloudflare configurations to your environment variables as follows:

```bash
export CLOUDFLARE_AUTH_EMAIL="Cloudflare account email"
export CLOUDFLARE_AUTH_KEY="Cloudflare API Key"
export CLOUDFLARE_ZONE_ID="Your zone ID"
```

### Running the script


```bash
wget -O - https://raw.githubusercontent.com/Olfredos6/cloudflary.py/main/cloudflary.py | python3 - [command] [arguments]
```

#### Available commands

- **list**: List all records on the specified zone(See ZONE_ID). <br>`list`
- **update**: Patch/Update a DNS record. This can be any value on the DNS record. <br>`update --record-id RECORD_ID --payload '{"key": "value"}'`
-  **get**: Get details of a DNS record.<br>`get --record-id RECORD_ID`


### Example
- Simple example:
  ```bash
  wget -O - https://raw.githubusercontent.com/Olfredos6/cloudflary.py/main/cloudflary.py |python3 - update --record-id 8ec292220081262ca459013e40f80df5 --payload '{"content": "142.251.47.78"}'
  ```

> 142.251.47.78 is Google :sweat_smile:

- One more realistic example: Automatically grab host's public IP from an Amazon EC2 instance and update a Cloudflare record
  ```bash
  wget -O - https://raw.githubusercontent.com/Olfredos6/cloudflary.py/main/cloudflary.py |python3 - update --record-id 8ec292220081262ca459013e40f80df5 --payload "{\"content\": \"$(curl -s ifconfig.me)\"}"
  ```
