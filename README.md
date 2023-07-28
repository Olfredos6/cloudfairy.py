
# A Python script for patching a Cloudflare's DNS record.

If you are using Cloudflare as CDN or proxy to a server with no reserved IP address from a cloud provider, you could use this script to run when switched on to update your records as desired.

Say you have the following records on Cloudflare:
![Alt text](image.png)

The `test` server is frequently switched on and off and its IP address changes every time it is started. Running this script by passsing it the ID of the record and the content to use as new records in a Python dictionary-like string will update the specified record.

## How to use it
### Prerequisites
Simply make sure you have `wget` or similar tool installed and download this script:
```bash
wget 
```

