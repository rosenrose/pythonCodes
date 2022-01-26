import subprocess
import sys
import shutil
from pathlib import Path

input = Path("Y:/")
output = Path("C:/Users/crazy/Pictures/temp")

for gif in sorted(input.glob("2021-06-12 오후 8*.gif")):
    subprocess.run(["ffmpeg","-i",gif,output/"temp"/"%04d.png","-y"])
    count = len(list(output.glob("*.png")))
    for i,png in enumerate((output/"temp").iterdir()):
        shutil.move(png,output/f"{count+i+1:04}.png")
subprocess.run(["ffmpeg","-framerate","20","-i",output/"%04d.png","-crf","19",output/"_.mp4","-y"])