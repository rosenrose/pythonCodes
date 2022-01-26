import json
import subprocess
from pathlib import Path
from PIL import Image, ImageSequence

path = Path("E:/Enjoy/")
animated = []
for anim in [*path.glob("*.webp"),*path.glob("*.gif")]:
    if (img:=Image.open(anim)).is_animated:
        animated.append(anim.name)
        # subprocess.run(["ffmpeg","-i",anim,"-frames","1",path/f"thumb/{anim.stem}.jpg"])
        if not (frame := path/f"thumb/{anim.stem}.png").exists():
            ImageSequence.Iterator(img)[0].save(frame)
# with open(webp,"rb") as f:
#     f.read(0x1E)
#     if f.read(4) == b"ANIM":
#         animated.append(webp.name)
html = open(path / "viewer.html",encoding="utf-8").read().splitlines()
for i,line in enumerate(html):
    if line.strip().startswith("list = "):
        html[i] = f"        list = {json.dumps(sorted(animated),ensure_ascii=False)};"
        break
open(path / "viewer.html","w",encoding="utf-8").write("\n".join(html))