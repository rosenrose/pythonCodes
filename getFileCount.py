from pathlib import Path
import sys

option = ""

if "-prefix" in sys.argv:
    folderList = [(Path(sys.argv[2])/i).resolve() for i in sys.argv[3:]]
else:
    folderList = [Path(i).resolve() for i in sys.argv[1:]]

result = 0
for folder in folderList:
    if option == "only code":
        for dir in [i for i in folder.iterdir() if i.is_dir()]:
            result = result + len(list(dir.iterdir()))
    else:
        result = result + len([i for i in folder.rglob("*") if i.is_file()])
print(result)