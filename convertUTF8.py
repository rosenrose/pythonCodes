# -*- coding: utf-8 -*-
import cchardet as chardet
import sys
import shutil
from pathlib import Path

extList = [".c",".cpp",".h",".hpp",".js",".txt"]
success = []
fail = []

def convert(file):
    data = open(file,"rb").read()
    result = chardet.detect(data)

    if (confidence := result['confidence']) is None or confidence <= 0.5:
        fail.append(f"Fail: {result}")
        #print(f"Fail: {result}")
        subprocess.run(["notepad++.exe",file])
        return

    codePage = result['encoding']
    success.append(f"{file} codePage: {codePage}")
    #print(f"{name} codePage: {codePage}")
    open(file,"wb").write(data.decode(codePage).encode("utf-8"))

if __name__ == "__main__":
    if (mode := sys.argv[1]) == "line":
        print(input().encode("cp949").decode("cp932"))
    elif mode == "file":
        convert(sys.argv[2])
    elif mode == "folder":
        folder = Path(sys.argv[2]).resolve()
        shutil.copytree(folder,old:=(folder.parent/"old"))

        for file in folder.rglob("*"):
            if file.suffix in extList:
                convert(str(file))
        shutil.move(old,folder)
    for m in success+fail:
        print(m)