import json
import sys
import shutil
import re
import pyperclip
from pathlib import Path
from functools import reduce
from PIL import Image, ImageChops

path = Path("d:/git/djmax/ignore/Sprite")

# img = Image.open(path / "Outgame_7.png")
img = Image.open(r"C:\Users\crazy\Pictures\Djmax Respect V\Djmax Respect V Screenshot 2022.02.01 - 12.47.50.82.png")

def itemCrop(x, y, w, h, cols, rows, pt, colgap = 2, rowcap = 2, colsFirst = False):
    if colsFirst:
        for j in range(rows):
            for i in range(cols):
                img.crop((x + (i * w) + (i * colgap), y + (j * h) + (j * rowcap), x + (i * w) + (i * colgap) + w, y + (j * h) + (j * rowcap) + h)).save(path / f"{pt}_{j+1:02}_{i+1:02}.png")
    else:
        for i in range(cols):
            for j in range(rows):
                img.crop((x + (i * w) + (i * colgap), y + (j * h) + (j * rowcap), x + (i * w) + (i * colgap) + w, y + (j * h) + (j * rowcap) + h)).save(path / f"{pt}_{i+1:02}_{j+1:02}.png")

plateWidth, plateHeight = 250, 60
# itemCrop(1851, 39, plateWidth, plateHeight, 2, 8, "plate/pt1")
# itemCrop(2512, 20, plateWidth, plateHeight, 6, 65, "plate/pt2")
# itemCrop(4024, 3988, plateWidth, plateHeight, 3, 1, "plate/pt3")
# itemCrop(101, 18, plateWidth, plateHeight, 1, 1, "plate/pt4")
# itemCrop(365, 20, plateWidth, plateHeight, 1, 1, "plate/pt5")
# itemCrop(2119, 634, plateWidth, plateHeight, 1, 1, "plate/pt6")
# itemCrop(2218, 1029, plateWidth, plateHeight, 1, 7, "plate/pt7")

iconWidth, iconHeight = 60, 60
# itemCrop(4186, 32, iconWidth, iconHeight, 1, 22, "icon/pt1")
# itemCrop(4186, 1520, iconWidth, iconHeight, 1, 36, "icon/pt2")
# itemCrop(4257, 60, iconWidth, iconHeight, 1, 22, "icon/pt3")
# itemCrop(4257, 1858, iconWidth, iconHeight, 1, 27, "icon/pt4")
# itemCrop(4366, 3016, iconWidth, iconHeight, 1, 13, "icon/pt5")
# itemCrop(2442, 2187, iconWidth, iconHeight, 1, 3, "icon/pt6")
# itemCrop(1785, 47, iconWidth, iconHeight, 1, 3, "icon/pt7")
# itemCrop(737, 859, iconWidth, iconHeight, 1, 1, "icon/pt8")
# itemCrop(744, 1983, iconWidth, iconHeight, 1, 2, "icon/pt9")
# itemCrop(4118, 2946, iconWidth, iconHeight, 1, 1, "icon/pt10")
# itemCrop(4116, 3126, iconWidth, iconHeight, 1, 1, "icon/pt11")
# itemCrop(4116, 3218, iconWidth, iconHeight, 1, 1, "icon/pt12")
# itemCrop(4117, 3447, iconWidth, iconHeight, 1, 1, "icon/pt13")

ngWidth, ngHeight = 50, 50
# itemCrop(4366, 40, ngWidth, ngHeight, 1, 49, "notegear/pt1")
# itemCrop(4428, 8, ngWidth, ngHeight, 1, 43, "notegear/pt2")
# itemCrop(4428, 2296, ngWidth, ngHeight, 1, 24, "notegear/pt3")
# itemCrop(2457, 4, ngWidth, ngHeight, 1, 2, "notegear/pt4")
# itemCrop(2460, 1735, ngWidth, ngHeight, 1, 1, "notegear/pt5")
# itemCrop(2460, 1823, ngWidth, ngHeight, 1, 1, "notegear/pt6")
# itemCrop(2460, 1911, ngWidth, ngHeight, 1, 1, "notegear/pt7")
# itemCrop(2460, 1999, ngWidth, ngHeight, 1, 1, "notegear/pt8")
# itemCrop(2460, 2087, ngWidth, ngHeight, 1, 1, "notegear/pt9")
# itemCrop(4499, 3638, ngWidth, ngHeight, 1, 1, "notegear/pt10")
# itemCrop(4134, 3512, ngWidth, ngHeight, 1, 2, "notegear/pt11")
# itemCrop(4133, 3621, ngWidth, ngHeight, 1, 2, "notegear/pt12")

commentWidth, commentHeight = 250, 60
itemCrop(426, 396, commentWidth, commentHeight, 4, 5, "comment/pt7", 16, 16, True)