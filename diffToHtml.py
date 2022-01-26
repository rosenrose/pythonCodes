import sys
from pathlib import Path

path = Path(sys.argv[1])
data = path.read_text(encoding="utf-8").splitlines()
diffs = []
temp = []

for line in data:
    if line.startswith("diff --git") and temp:
        diffs.append(temp)
        temp = []
    else:
        temp.append(line)
diffs.append(temp)

template = Path("C:/Users/crazy/Pictures/python/diffTemplate.html").read_text(encoding="utf-8")
for i,diff in enumerate(diffs):
    diffString = template.replace("{}","\n".join(diff).replace("\\","\\\\"))
    Path(path.parent/f"diff_{i}.html").write_text(diffString,encoding="utf-8")