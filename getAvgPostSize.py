from pathlib import Path
import sys

path = Path("D:/touhou/doujin")
folderList = ["dcinside","enlsparker","ghap","ghapgithub","lilybin","nonicname","ruliweb","rumia0528","seiga22",
                "sniperriflesr","sunmism","touhoustory"]
KILO = 1024
KB = KILO
MB = KILO**2
GB = KILO**3

postCount = 0
totalSize = 0
for folder in folderList:
    for dir in [i for i in (path/folder).iterdir() if i.is_dir()]:
        postCount+=1
        for file in dir.iterdir():
            totalSize = totalSize + file.stat().st_size

print(f"posts: {postCount}, size: {totalSize/GB:.2f}, avg: {(totalSize/postCount)/MB:.2f}")
