import sys
from pathlib import Path
from PIL import Image

datPath = Path(sys.argv[1])
base = Image.open(datPath/sys.argv[2])
exList = ["bs","bsl","bs2","ct"]
if "enemy" in str(datPath):
    normals = [Image.open(i) for i in datPath.glob("face????.png") if i.stem[-2:] not in exList]
    loses = [Image.open(i) for i in datPath.glob("face????l.png") if i.stem[-3:] not in exList]
else:
    normals = [Image.open(i) for i in datPath.glob("face_pl????.png") if i.stem[-2:] not in exList]
    loses = []

with (datPath/"face.txt").open(encoding="utf-8") as f:
    args = f.read().splitlines()
smallCrop = [int(i) for i in args[0].split(":")]
blank = Image.new("RGBA",(smallCrop[0],smallCrop[1]))
smallCrop = (smallCrop[2],smallCrop[3],smallCrop[2]+smallCrop[0],smallCrop[3]+smallCrop[1])
overlay = tuple(int(i) for i in args[1].split(":"))
if len(args) > 2:
    bigCrop = [int(i) for i in args[2].split(":")]
    bigCrop = (bigCrop[2],bigCrop[3],bigCrop[2]+bigCrop[0],bigCrop[3]+bigCrop[1])

if not (datPath/"new").exists():
    (datPath/"new").mkdir()
if base.filename.endswith("bs.png"):
    for normal in normals:
        new = base.copy()
        new.paste(blank, overlay)
        new.paste(normal.crop(smallCrop), overlay)
        if len(args) > 2:
            new = new.crop(bigCrop)
        new.save(datPath/f"new/normal_{Path(normal.filename).name}")
else:
    for lose in loses:
        new = base.copy()
        new.paste(blank, overlay)
        new.paste(lose.crop(smallCrop), overlay)
        new.save(datPath/f"new/lose_{Path(lose.filename).name}")

# game = sys.argv[1]
# folder = sys.argv[2]
# prefix = sys.argv[3]
# mode = sys.argv[4]
# background = sys.argv[5]
# default = sys.argv[6]
# workDir = datPath/game/"face"/folder

# with (workDir/"face.txt").open(encoding="utf-8") as f:
#     args = f.read().splitlines()

# if len(args) < 3:
#     overlay = tuple([int(i) for i in args[0].split(":")])
#     smallImg = Image.open(workDir/(prefix+default))
#     bigImg = Image.open(workDir/(prefix+background))
#     smallCrop = (smallImg.width,smallImg.height,0,0)
#     bigCrop = (bigImg.width,bigImg.height,0,0)
# else:
#     smallCrop = [int(i) for i in args[0].split(":")]
#     overlay = tuple([int(i) for i in args[1].split(":")])
#     bigCrop = [int(i) for i in args[2].split(":")]

# blank = Image.new("RGBA",(smallCrop[0],smallCrop[1]))
# smallCrop = (smallCrop[2],smallCrop[3],smallCrop[2]+smallCrop[0],smallCrop[3]+smallCrop[1])
# bigCrop = (bigCrop[2],bigCrop[3],bigCrop[2]+bigCrop[0],bigCrop[3]+bigCrop[1])

# exList = ["bs.png","bs_.png","bsl.png","bs2.png","ct.png"]
# exList.append(background)
# if "17" not in game and game != "th12":
#     exList.append("lo.png")

# bs = Image.open(workDir/(prefix+background))
# ntemplate = bs.copy()
# ntemplate.paste(blank,overlay)
# if "17" in game and "enemy" in folder:
#     bsl = Image.open(workDir/f"{prefix}bsl.png")
#     ltemplate = bsl.copy()
#     ltemplate.paste(blank,overlay)

# for i in workDir.glob(prefix+"*_b.png"):
#     name = i.name()[len(prefix):]
#     if name not in exList:
#         face = Image.open(i)
#         if mode == "paste":
#             temp = ntemplate.copy()
#             temp.paste(face.crop(smallCrop),overlay)
#         elif mode == "alpha":
#             temp = bs.copy()
#             temp.alpha_composite(face.crop(smallCrop),overlay)
#         if game == "th14" and background == "bs2.png":
#             temp.crop(bigCrop).save(workDir/f"normal2_{prefix}{name}")
#         else:
#             temp.crop(bigCrop).save(workDir/f"normal_{prefix}{name}")
#         if "17" in game and "enemy" in folder:
#             temp = ltemplate.copy()
#             temp.paste(face.crop(smallCrop),overlay)
#             temp.crop(bigCrop).save(workDir/f"lose_{prefix}{name}")

# face = Image.open(workDir/(prefix+default))
# if mode == "paste":
#     temp = ntemplate.copy()
#     temp.paste(face.crop(smallCrop),overlay)
# elif mode == "alpha":
#     temp = bs.copy()
#     temp.alpha_composite(face.crop(smallCrop),overlay)
# temp.save(workDir/f"{prefix}{+background.split('.')[0]}_.{background.split('.')[-1]}")