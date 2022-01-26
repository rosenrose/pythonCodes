from pathlib import Path
import os
import sys

path = Path(sys.argv[1]).resolve()
result=[]

for dir in path.rglob("*"):
    if os.access(dir,os.R_OK) and dir.is_dir():
        result.append([len([i for i in dir.iterdir() if i.is_file()]),dir])

result = sorted(result, key=lambda arg: arg[0])
print(*result,sep="\n")