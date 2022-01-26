import sys
from pathlib import Path

folder = Path(sys.argv[1]).resolve()
artist = input("artist: ")
album = input("album: ")
#titleSlice = [int(i) for i in input("title slice: ").split(",")]

for i,file in enumerate(folder.iterdir()):
    titleSlice = [0,str(file).find(']')+1]
    file.rename(file.with_name(f"{artist}-{album}-{i+1:02d}-{str(file)[0:titleSlice[0]]+str(file)[titleSlice[1]+1:]}"))