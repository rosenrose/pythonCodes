import pyperclip
import requests
import urllib
import sys
import time
import shutil
import json
from pathlib import Path

cookie = json.load(open("c:/users/crazy/pictures/python/cookie.json",encoding="utf-8"))
cookie = {c["name"]: c["value"] for c in cookie["pixiv"]}

path = Path(sys.argv[1])
if not path.exists():
    path.mkdir(parents=True)

if sys.argv[2] == "clip":
    images = pyperclip.paste().splitlines()
elif sys.argv[2] == "input":
    images = sys.argv[3:]

for url in images:
    name = urllib.parse.unquote(url.split("/")[-1])
    # name = name[:name.find("?")]+".jpg"
    output = path / name

    # urllib.request.urlretrieve(url, output)
    with requests.get(url,stream=True,cookies=cookie) as result:
        with open(output,"wb") as f:
            shutil.copyfileobj(result.raw,f,length=16*1024*1024)

    print(f"download: {output}")
    time.sleep(1)

# for (a of document.querySelector("#post-4234 > div.entry-content > figure:nth-child(9) > ul").querySelectorAll("img")){
#   b = /(.+?)(-\d{3,4}x\d{3,4})?(\.(jpg|jpeg|png))/.exec(a.src);
#   console.log(b[1]+b[3]);
# }