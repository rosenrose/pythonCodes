from pathlib import Path
import sys

if "-prefix" in sys.argv:
    folderList = [(Path(sys.argv[2])/i).resolve() for i in sys.argv[3:]]
else:
    folderList = [Path(i).resolve() for i in sys.argv[1:]]

for folder in folderList:
    dirs = [i for i in folder.iterdir() if i.is_dir()]
    files = [i for i in folder.iterdir() if str(i).endswith(".html")]
    if len(dirs) != len(files):
        for i in range(min(len(dirs),len(files))):
            print([dirs[i],files[i]])
