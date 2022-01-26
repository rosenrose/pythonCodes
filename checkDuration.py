import subprocess
import json
import sys
from pathlib import Path

path = Path("D:/Touhou/OST")

result = []
for data in list(path.rglob("*.opus"))+list(path.rglob("*.m4a")):
    p = subprocess.run(["ffprobe","-i",data,"-of","json","-show_format"],capture_output=True)
    output = json.loads(p.stdout.decode("utf-8"))
    if (p.returncode == 1):
        print(data,"returncode 1")
        break
    else:
        duration = float(output["format"]["duration"])
        result.append((duration, str(data.relative_to(data.parents[2]))))
result.sort(key=lambda x: -x[0])
print(*result,sep="\n")

# p = subprocess.run(["ffprobe","-i",data,"-of","json","-show_format"],stderr=sys.stderr)
# p = subprocess.Popen(["ffmpeg","-i","c:/users/crazy/pictures/destiny.mp3","c:/users/crazy/pictures/out.mp3","-y"],stderr=subprocess.PIPE)
# while True:
#     output = p.stderr.readline()
#     if output == "" and p.poll() is not None:
#         break
#     if output:
#         print(output)
# rc = p.poll()