import sys
import pdf2image
from pathlib import Path

pdf = sys.argv[1]
dest = Path(sys.argv[2])

pages = pdf2image.convert_from_path(pdf)
for i, page in enumerate(pages):
    page.save(dest/f"{i:03}.png", "PNG")