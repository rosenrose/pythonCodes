import sys
from pathlib import Path
from PIL import Image

path = Path("c:/users/crazy/pictures/Djmax Respect V")
x,y = 69,0
w,h = 502,744
newLength = 23
images = [i.name for i in path.glob("z*.png")]
startImgName = f"{sys.argv[1]}.png"
startImage = Image.open(path/startImgName)
startImage = startImage.crop((x,y,x+w,y+h))
restImages = [Image.open(path/i) for i in images[images.index(startImgName)+1:]]
total = len(restImages)
for i,rest in enumerate(restImages):
    new = Image.new("RGB", (w,startImage.height+newLength))
    new.paste(startImage, (0,newLength))
    restCrop = rest.crop((x,y,x+w,y+newLength))
    new.paste(restCrop, (0,0))
    startImage = new
    if i%10 == 0:
        print(i, total)
startImage.save(path/"_.png")
