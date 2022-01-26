import sys
import zlib
import hashlib

try:
    file = open(sys.argv[2],"rb").read()
except:
    file = sys.argv[2].encode("utf-8")

if sys.argv[1] == "crc32":
    crc = zlib.crc32(file)
    crc = crc & 0xFFFFFFFF      # 32비트 unsigned 형으로 변환
    print(f"{crc:X}\n{crc}")
elif sys.argv[1] == "sha256":
    sha = hashlib.sha256(file).hexdigest()
    print(sha)