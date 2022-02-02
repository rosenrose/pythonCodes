import subprocess
import json
import sys
import re
import pyperclip
import requests

urlReg = re.compile(r"https://www.youtube.com/watch\?v=([a-zA-Z0-9_\-]{11})")
lengthReg = re.compile(r"PT(\d+)M((\d+)S)?")
key = open("youtubeAPI.txt",encoding="utf-8").read()

def getDuration(url):
    id = urlReg.search(url)[1]
    result = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={id}&key={key}&part=contentDetails")
    duration = json.loads(result.content)["items"][0]["contentDetails"]["duration"]
    duration = lengthReg.search(duration)
    return int(duration[1])*60 + (int(duration[3]) if duration[2] else 0)

if len(sys.argv) < 2:
    while (url:=input("주소: ")) != "q":
        print(getDuration(url))
else:
    data = json.load(open("d:/git/djmax.github.io/list.json",encoding="utf-8"))
    dlc = sys.argv[1]
    start = int(sys.argv[2])
    for i,song in enumerate(data[dlc][start:]):
        print(i+start,title:=song["title"])
        pyperclip.copy(title)
        # url = urlReg.search(input("주소: "))[0]
        # p = subprocess.run(["youtube-dl","-g",url],capture_output=True)
        # url = p.stdout.decode("utf-8").splitlines()[0]
        # p = subprocess.run(["ffprobe","-i",url,"-of","json","-show_format"],capture_output=True)
        # duration = json.loads(p.stdout.decode("utf-8"))["format"]["duration"]
        data[dlc][i+start]["length"] = getDuration(input("주소: "))
        json.dump(data,open("d:/git/djmax.github.io/list.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
        print(data[dlc][i+start]["length"],"\n")