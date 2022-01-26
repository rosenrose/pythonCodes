import sys
import subprocess
from pathlib import Path

for file in [Path(i) for i in sys.argv[1:]]:
    data = file.read_text(encoding="utf-8").splitlines()

    with open(new:=file.with_stem(file.stem+"_"),"w") as f:
        for line in data:
            pos1 = line.find("|")
            pos2 = line.find("|",pos1+1)
            f.write(line[:pos2].rstrip()+"\n")

    subprocess.run(["notepad++.exe",new])