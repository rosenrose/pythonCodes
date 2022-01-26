import subprocess
import json
import sys
from pathlib import Path

source=Path("D:/Obb/data")

for data in source.iterdir():
    if(sys.argv[1] == "check"):
        p = subprocess.run(["ffprobe", "-i", data, "-show_format", "-of", "json"], capture_output=True)
        output = json.loads(p.stdout.decode("utf-8"))
        if (p.returncode == 1):
            data.unlink()
        else:
            if((fileFormat := "."+output["format"]["format_name"]) != ".mp3"):
                print(data, fileFormat, sep="\t")
            if(data.suffix != ".mp3"):
                data.rename(data.with_suffix(fileFormat))
    elif(sys.argv[1] == "name"):
        with data.open("rb") as f:
            f.seek(0x1004)
            name = bytes(0)
            while((byte:=f.read(1)) != b'\x00' and byte != b'\x02'):
                name += byte
        name = name.decode()
        if not (new:=data.with_suffix(".mp3")).exists():
            data.rename(new)

# p = subprocess.run(["ffprobe","-i",data,"-of","json","-show_format"],stderr=sys.stderr)
# p = subprocess.Popen(["ffmpeg","-i","c:/users/crazy/pictures/destiny.mp3","c:/users/crazy/pictures/out.mp3","-y"],stderr=subprocess.PIPE)
# while True:
#     output = p.stderr.readline()
#     if output == "" and p.poll() is not None:
#         break
#     if output:
#         print(output)
# rc = p.poll()