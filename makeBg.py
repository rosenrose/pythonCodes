import sys
import os
from glob import glob
from PIL import Image

#game=sys.argv[1]
#datPath="d:/touhou/touhousuperextractor1.2.5/%s/background"%(game)
datPath = "D:/Touhou/TouhouSuperExtractor1.2.5/PC98dats/th02/MIMA"
"""folders = ["bg%02d"%i for i in range(0,19)]
folders.remove("bg07")
folders.remove("bg08")
folders.remove("bg09")"""
"""folders=["bg17"]
folders=["bg%02d"%i for i in range(30,39)]
folders.remove("bg35")"""
#folders=["bg34"]

for folder in [datPath]:
    #os.chdir(datPath+"/"+folder)
    os.chdir(datPath)
    x = 0
    y = 0
    #result = Image.new("RGBA",(256*5+120,256*4+176))
    result = Image.new("RGBA",(256,256))
    i = 0
    for bg in glob("*.png"):
        chunk = Image.open(bg)
        result.paste(chunk,(x,y))
        x+=chunk.width
        if (i+1)%8 == 0:
            x=0
            y+=chunk.height
        i+=1
    result = result.crop((0,0,result.width,y))
    #result.save("../%s.png"%(folder))
    result.save("0.png")