import sys
from pathlib import Path

path = Path(sys.argv[2]).resolve()
excludes = [".git","__pycache__","__init__.py"]

def exclude(path):
    # if set(path.parts) & set(excludes):
    #     return False
    for part in path.parts:
        for exclude in excludes:
            if part.startswith(exclude):
                return False
    return True

for file in [i for i in path.rglob("*") if i.is_file() and exclude(i)]:
    try:
        file.open(encoding="utf-8").readline()
    except:
        # print(f"{file.relative_to(path)} -- Binary")
        pass
    else:
        if b"\r\n" in (line:=file.open("rb").readline()):
            print(f"{file.relative_to(path)} -- CRLF")
            if sys.argv[1] == "tolf":
                data = file.read_text(encoding="utf-8")
                file.open("w",encoding="utf-8",newline="\n").write(data)
                print(f"--- convert {file.relative_to(path)} to LF ---")
        elif b"\n" in line:
            print(f"{file.relative_to(path)} -- LF")
            if sys.argv[1] == "tocrlf":
                file.write_text(file.read_text(encoding="utf-8"),encoding="utf-8")
                print(f"--- convert {file.relative_to(path)} to CRLF ---")