from pathlib import Path
import sys

path = Path(sys.argv[1]).resolve()
print(*[f'"{f.name}"' for f in path.iterdir() if f.is_file()],sep=" ")