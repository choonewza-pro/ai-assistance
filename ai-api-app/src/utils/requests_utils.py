import os
import requests

def patched_get(url, *args, **kwargs):
    headers = kwargs.pop("headers", {})
    headers["User-Agent"] = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    return requests.get(url, headers=headers, *args, **kwargs)