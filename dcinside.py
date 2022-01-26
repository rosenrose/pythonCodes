import requests
import time
from hashlib import sha256
from base64 import b64encode
from urllib.parse import urlencode

XML_HTTP_REQ_HEADERS = {
    "Accept": "*/*",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
s = requests.session()
payload = {"id": "rayarkcytus", "no": 59348, "cpage": 1, "managerskill":"", "del_scope": "1", "csort": ""}
res = s.post("https://m.dcinside.com/ajax/response-comment", headers=XML_HTTP_REQ_HEADERS, data=payload)
print(res.text)