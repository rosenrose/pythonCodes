import sys
import os
from glob import glob
from PIL import Image
from functools import reduce

def drawLine(image,x,y,width,height):
    for i in range(x-1,x+width+1):
        image.putpixel((i,y-1),(0,0,0))
#num=sys.argv[1]
#datPath="D:/Touhou/TouhouSuperExtractor1.2.5/th155/backGround/mob"
folder=sys.argv[1]
datPath="D:/Touhou/TouhouSuperExtractor1.2.5/th075/character/"+folder
os.chdir(datPath)
cols = 10
fileList = glob("*")
rows = int((len(fileList)-1)/10)+1
print(rows)

images = []
for i in range(rows):
    print([j for j in fileList[i*10:(i+1)*10]])
    images.append([Image.open(j) for j in fileList[i*10:(i+1)*10]])
#input(images)
x=0
y=0
for i in images:
    width = reduce(lambda x,y:x+y, [j.width for j in i])
    if x<width:
        x=width
    y += max([j.height for j in i])
print((x,y))
result = Image.new("RGBA",(x+cols-1,y+rows-1))

y=0
for i in images:
    width = reduce(lambda x,y:x+y, [j.width for j in i])
    x=0
    for j in i:
        result.paste(j,(x,y))
        x+=(j.width+1)
    maxHeight = max([j.height for j in i])
    y += maxHeight
    x=0
    for j in i:
        x+=(j.width)
        if x<result.width:
            for z in range(y-maxHeight,y):
                result.putpixel((x,z),(0,0,0))
        x+=1
    if y<result.height:
        for z in range(min(width+cols,result.width)):
            result.putpixel((z,y),(0,0,0))
    if y-maxHeight-1>0:
        for z in range(min(width+cols,result.width)):
            result.putpixel((z,y-maxHeight-1),(0,0,0))
    y+=1
result.save("0.png")

"""
chars = [i[:-8] for i in glob("*0000.png")]
for char in chars:
    lists = glob(char+"0*.png")
    if len(lists) < 2:
        print(char)
        continue
    images=[Image.open(i) for i in lists]
    resultWidth = reduce((lambda x,y: x+y),[i.width for i in images])
    result = Image.new("RGBA",(resultWidth,images[0].height))
    x=0
    for i in range(len(images)):
        result.paste(images[i],(x,0))
        x+=images[i].width
    result.save("mob/%s.png"%(char))
"""