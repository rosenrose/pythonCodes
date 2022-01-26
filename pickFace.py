import sys
import os
import shutil
from glob import glob
from PIL import Image

game = sys.argv[1]
datPath="D:/Touhou/TouhouSuperExtractor1.2.5/"+game
charList = ["doremy","futo","hijiri","ichirin","jyoon","kasen","koishi","kokoro","mamizou","marisa","miko","mokou","nitori","reimu","shion","sinmyoumaru","tenshi","usami","udonge","yukari"]

for char in charList:
    if not os.path.exists(datPath+"/actor/"+char):
        continue
    os.chdir(datPath+"/actor/"+char)
    for i in glob("*.png"):
        img = Image.open(i)
        if img.width > 400 and img.height>400:
            print(char+": copy "+i)
            #shutil.copy(i,"%s/system/char_def/face/%s"%(datPath,char))
            shutil.copy(i,"%s/event/pic/%s"%(datPath,char))
            
    if not os.path.exists(datPath+"/actor/"+char+"/texture"):
        continue
    os.chdir(datPath+"/actor/"+char+"/texture")
    for i in glob("*.png"):
        img = Image.open(i)
        if img.width > 400 and img.height>400:
            print(char+": copy "+i)
            #shutil.copy(i,"%s/system/char_def/face/%s"%(datPath,char))
            shutil.copy(i,"%s/event/pic/%s"%(datPath,char))
            