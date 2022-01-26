#-*-coding:utf-8
import re
import sys
from pathlib import Path

smi = Path(sys.argv[1]).resolve()
data = smi.read_text(encoding="utf-8").splitlines()
for i,line in enumerate(data):
    if line.startswith("<SYNC Start="):
        result = re.compile(r".*?=(\d+)>.*").search(line)
        sync = result.group(1)
        data[i] = line.replace(sync, str(int(sync)+int(sys.argv[2])))
smi.with_stem(smi.stem+"_new").write_text("\n".join(data),encoding="utf-8")