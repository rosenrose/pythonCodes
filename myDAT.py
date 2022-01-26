import sys
from pathlib import Path

def pack(folder,archive):
    fileList = [{"name":str(i.relative_to(folder)), "size": i.stat().st_size} for i in folder.rglob("*") if i.is_file()]
    print(*fileList,sep="\n")

    with archive.open("wb") as f:
        f.write(b'mypk')
        f.write(len(fileList).to_bytes(2,"big"))
        for file in fileList:
            f.write(file["name"].encode("utf-8"))
            f.write(b'\x00')
            f.write(file["size"].to_bytes(4,"big"))
        for file in fileList:
            f.write((folder/file["name"]).read_bytes())
        f.close()

def unpack(archive,folder):
    f = archive.open("rb")
    f.read(4)
    fileCount = int.from_bytes(f.read(2),"big")
    fileList = []
    for _ in range(fileCount):
        fileName = bytes(0)
        while((byte:=f.read(1)) != b'\x00'):
            fileName += byte
        fileName = fileName.decode("utf-8")
        fileSize = int.from_bytes(f.read(4),"big")
        fileList.append({"name":fileName,"size":fileSize})
    print(fileList)
    
    for file in fileList:
        outPath = (folder/file["name"]).parent
        if not outPath.exists():
            outPath.mkdir(parents=True)
        (folder/file["name"]).write_bytes(f.read(file["size"]))
    f.close()

if sys.argv[1] == "pack":
    pack(Path(sys.argv[2]).resolve(),Path(sys.argv[3]).resolve())
elif sys.argv[1] == "unpack":
    unpack(Path(sys.argv[2]).resolve(),Path(sys.argv[3]).resolve())