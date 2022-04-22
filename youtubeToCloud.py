import sys
import re
import subprocess
from pathlib import Path
from yt_dlp import YoutubeDL

def main(url):
    id = re.search(r"[0-9a-zA-Z_\-]{11}", url)[0]

    with YoutubeDL({"simulate": True}) as ydl:
        info = ydl.extract_info(url)
    
    for format in info["requested_formats"]:
        if format["vcodec"] != "none":
            src = format["url"]
    # print(src)

    proc = subprocess.run(["ffmpeg", "-i", src, "-f", "image2pipe", "-vf", "fps=12", "-q:v", "4", "-c:v", "mjpeg", "pipe:1"], capture_output=True)
    output = proc.stdout
    jpg_head = b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46"
    jpgs = [jpg_head + i for i in output.split(jpg_head)[1:]]
    print(id, len(output)/(1024**2), len(jpgs))

    for i, jpg in enumerate(jpgs):
        p = subprocess.Popen([
            "rclone",
            "--dry-run",
            "rcat",
            f"amazon_rosenrose:/rosenrose/djmax/bga/{id}/{i+1:04}.jpg",
            "-v"
            ], stdin=subprocess.PIPE, stdout=sys.stdout)
        p.stdin.write(jpg)
        p.stdin.close()
        # while msg := p.stdout.read():
        #     print(msg.decode("utf-8"))
        p.terminate()
        # (idCut := Path(f"E:/DJMAX MV/cut/{id}")).mkdir(exist_ok=True)
        # (idCut/f"{i+1:04}.jpg").write_bytes(jpg)

if __name__ == "__main__":
    main(sys.argv[1])