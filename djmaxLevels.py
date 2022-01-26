from PIL import Image, ImageChops
from pathlib import Path
import sys
import json
import pyautogui
import time

x,y = 116,540
gap = 342/14

def getlevel():
    img = pyautogui.screenshot()
    level = 0
    while ((pix:=img.getpixel((round(x+level*gap),y))) != (0,0,0)) and level<15:
        # print(pix)
        level += 1
    # print(pix)
    return level

def check():
    path = Path("C:/Users/crazy/Pictures/Djmax Respect V")
    songList = json.load(open("d:/git/djmax.github.io/list.json",encoding="utf-8"))
    songList["리스펙트"].insert(4,songList["테크니카 3"].pop())
    songList["리스펙트"].insert(7,songList["블랙 스퀘어"].pop())
    songList["리스펙트"].insert(19,songList["테크니카 1"].pop())
    songList["리스펙트"].insert(21,songList["테크니카 2"].pop())
    songList["리스펙트"].insert(40,songList["트릴로지"].pop())
    songList["리스펙트"].insert(47,songList["클래지콰이"].pop())
    collabo = ["길티기어","츄니즘","사이터스","디모","그루브 코스터","소녀전선"]
    # print(*[i["title"] for i in songList["리스펙트"]],sep="\n")
    songList = {i: songList[i] for i in [*list(songList.keys())[:-1*len(collabo)],*collabo]}
    checks = []
    time.sleep(3)
    for dlc in list(songList.keys())[1:]:
        # print(len(songList[dlc]), dlc)
        for song in songList[dlc]:
            for btn in song["level"]:
                for ptn in song["level"][btn]:
                    # print(f"{dlc}_{song['title']}_{btn}_{ptn}")
                    level = song["level"][btn][ptn]
                    getLv = getlevel()
                    for _ in range(2):
                        if level == getLv:
                            # checks.append((pyautogui.screenshot(),f"{dlc}_{song['title']}_{btn}_{ptn}_{level}={getLv}.png"))
                            # print(f"equal {level=}, {getLv=}")
                            break
                        else:
                            # print(getLv)
                            time.sleep(0.5)
                    # try:
                    assert level==getLv, f"{level=}, {getLv=}"
                    # except:
                    #     pyautogui.screenshot().save(path/"_.png")
                    if ptn != list(song["level"][btn].keys())[-1]:
                        pyautogui.press("right")
                        time.sleep(0.5)
                pyautogui.press("tab")
                time.sleep(0.5)
            pyautogui.press("down")
            time.sleep(0.5)
        if dlc not in collabo:
            pyautogui.press("shiftright",2)
            time.sleep(0.5)
    # for i in checks: i[0].save(path/i[1])

if sys.argv[1] == "check":
    check()
elif sys.argv[1] == "getlevel":
    while input("") != "q":
        print(getlevel())