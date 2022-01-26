import sys
import re
from pathlib import Path

end = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
lines = []
temp = []
for line in end:
    if line.startswith("@"):
        if temp:
            lines.append(temp)
        temp = []
    else:
        temp.append(line.replace("\x00","").strip())

regex = re.compile(r"\S+")
for j,line in enumerate(lines):
    for i in range(len(line)):
        if j in range(1,len(lines)-2):
            if i==0:
                if char := regex.match(line[i]):
                    line[i] = f"<tl${char[0]}:> " + line[i][char.end():].strip()
            else:
                line[i] = "<l$> " + line[i].strip()
        print(line[i])
    print("")
# print(*[i for line in lines for i in line],sep="\n")