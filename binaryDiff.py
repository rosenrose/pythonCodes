# -*- coding: utf-8 -*-
import sys
import zlib
from pathlib import Path

cmp1 = Path(sys.argv[1]).resolve()
cmp2 = Path(sys.argv[2]).resolve()

files1 = [f.name for f in cmp1.rglob("*") if f.is_file()]
files2 = [f.name for f in cmp2.rglob("*") if f.is_file()]

set1 = set(files1)
set2 = set(files2)
common = sorted(set1 & set2)
s1_only = sorted(set1 - set2)
s2_only = sorted(set2 - set1)

diff = [i for i in common if zlib.crc32((cmp1/i).read_bytes()) != zlib.crc32((cmp2/i).read_bytes())]

print("Diff")
print(*diff,sep="\n")
print("\nS1 only")
print(*s1_only,sep="\n")
print("\nS2 only")
print(*s2_only,sep="\n")