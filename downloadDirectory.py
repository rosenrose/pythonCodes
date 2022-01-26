import requests
import sys
import shutil
import time
from bs4 import BeautifulSoup
from pathlib import Path
from urllib import parse

def recur(url):
    with requests.get(url,stream=True) as result:
        path = parse.urlparse(url).path.removeprefix("/") # 앞에 / 있으면 pathlib에서 문제 발생
        if "Content-Type" in result.headers and "html" in result.headers["Content-Type"]:
            print(f"directory: {path}")
            soup = BeautifulSoup(result.text, "html.parser")
            for a in soup.select("a")[1:]:
                recur(parse.unquote(parse.urljoin(url,a["href"])))
        else:
            # print(f"file: {path}")
            output = dst / path
            if not output.parent.exists():
                output.parent.mkdir(parents=True)

            if output.exists():
                return

            try:
                with open(output,"wb") as f:
                    shutil.copyfileobj(result.raw,f,length=16*1024*1024)
                # time.sleep(5)
                print(f"download: {path}")
            except Exception as e:
                print(e)
                output.unlink()

# http://175.241.21.20:8800/
# dst = Path(sys.argv[1])
dst = Path("f:/175.241.21.20")
exception = []
for src in sys.argv[1:]:
    recur(parse.unquote(src))