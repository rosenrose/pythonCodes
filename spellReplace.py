import webbrowser
import re
import sys
import time
import pyautogui
import pyperclip
import requests
import datetime
from random import *
regex1 = re.compile("\[(br|BR|Br|bR)\]\s*「([^」]*[가-힣]+[^」]*)」")
regex2 = re.compile("([가-힣a-zA-Z0-9][^\s「|]*)[ ]*「([^」]*[가-힣]+[^」]*)」")
regex3 = re.compile("「([^」]*[가-힣]+[^」]*)」")
#regex3 = re.compile("[ᄀ-ᇿㄱ-\u318F가-힣\u2E80-\u2EFF㇀-\u31EF㈀-㋿]㐀-\u4DBF一-龿豈-\uFAFF𠀀-\U0002A6DF\U0002F800-\U0002FA1F\u3040-ゟ゠-ヿㇰ-ㇿ々〆〤！-～]")

charList={"th":["하쿠레이 레이무","키리사메 마리사"],
"th06":["루미아","치르노","홍 메이링","파츄리 널릿지","이자요이 사쿠야","레밀리아 스칼렛","플랑드르 스칼렛"],
"th07":["레티 화이트락","첸(동방 프로젝트)","앨리스 마가트로이드","프리즘리버 자매","콘파쿠 요우무","사이교우지 유유코","야쿠모 란","야쿠모 유카리"],
"th08":["리글 나이트버그","미스티아 로렐라이","카미시라사와 케이네","레이센 우동게인 이나바","야고코로 에이린","호라이산 카구야","후지와라노 모코우"],
"th075":["이부키 스이카"],
"th09":["샤메이마루 아야","메디슨 멜랑콜리","카자미 유카\u0014","오노즈카 코마치","시키에이키 야마자나두"],
"th10":["아키 시즈하\u0014","아키 미노리코","카기야마 히나","카와시로 니토리","이누바시리 모미지\u0014","코치야 사나에","야사카 카나코","모리야 스와코"],
"th105":["나가에 이쿠","히나나위 텐시"],
"th11":["키스메\u0014","쿠로다니 야마메","미즈하시 파르시","호시구마 유기","코메이지 사토리","카엔뵤 린","레이우지 우츠호","코메이지 코이시"],
"th12":["나즈린","타타라 코가사","쿠모이 이치린","무라사 미나미츠","토라마루 쇼","히지리 뱌쿠렌","호쥬 누에"],
"th123":["나마즈\u0014"],
"th125":["히메카이도 하타테\u0014"],
"th128":["서니 밀크\u0014","루나 차일드\u0014","스타 사파이어(동방 프로젝트)\u0014"],
"th13":["카소다니 쿄코","미야코 요시카","곽청아","소가노 토지코\u0014","모노노베노 후토","토요사토미미노 미코","후타츠이와 마미조"],
"th135":["하타노 코코로"],
"th14":["와카사기히메","세키반키","이마이즈미 카게로","츠쿠모 벤벤","츠쿠모 야츠하시","키진 세이자","스쿠나 신묘마루","호리카와 라이코"],
"th145":["이바라키 카센","우사미 스미레코"],
"th15":["세이란","링고(동방 프로젝트)","도레미 스위트","키신 사구메","클라운피스","순호","헤카티아 라피스라줄리"],
"th16":["이터니티 라바","사카타 네무노","릴리 화이트(동방 프로젝트)\u0014","코마노 아운","야타데라 나루미","테이레이다 마이","니시다 사토노","마타라 오키나"],
"th155":["요리가미 조온","요리가미 시온"],
"th17":["에비스 에이카","우시자키 우루미","니와타리 쿠타카","킷초 야치에","조토구 마유미","하니야스신 케이키","쿠로코마 사키"]}
grimari=["하쿠레이 레이무\u0014","루미아","리글 나이트버그","미즈하시 파르시","카와시로 니토리\u0014","레티 화이트락","홍 메이링","콘파쿠 요우무\u0014",
            "미스티아 로렐라이","카기야마 히나","쿠로다니 야마메","야쿠모 란","첸(동방 프로젝트)","카미시라사와 케이네\u0014","오노즈카 코마치","아키 미노리코",
            "이부키 스이카","호시구마 유기","시키에이키 야마자나두","메디슨 멜랑콜리","프리즘리버 자매","루나사 프리즘리버","메를랑 프리즘리버",
            "리리카 프리즘리버","치르노\u0014","야고코로 에이린\u0014","레이센 우동게인 이나바\u0014","호라이산 카구야\u0014","이나바 테위\u0014","카엔뵤 린",
            "레이우지 우츠호\u0014","야사카 카나코","모리야 스와코","앨리스 마가트로이드\u0014","파츄리 널릿지\u0014","레밀리아 스칼렛\u0014",
            "플랑드르 스칼렛\u0014","나가에 이쿠","사이교우지 유유코\u0014","코메이지 사토리\u0014","코메이지 코이시\u0014","이자요이 사쿠야\u0014",
            "코치야 사나에\u0014","후지와라노 모코우\u0014","키리사메 마리사\u0014","키스메","아키 시즈하","히나나위 텐시","샤메이마루 아야\u0014","야쿠모 유카리\u0014"]

def edit():
    data = pyperclip.paste()
    #with open("c:/users/crazy/pictures/python/temp.txt",encoding="utf-8") as a:
    #    data = a.read()
    """data = regex1.sub("[br]\"\g<2>\"",data)
    data = regex2.sub("\g<1> \"\g<2>\"",data)
    data = regex3.sub("\"\g<1>\"",data)"""
    data = data.replace("식륜","하니와").replace("방형","사각형").replace("아이돌라","이돌라")
    #with open("c:/users/crazy/pictures/python/temp.txt","w",encoding="utf-8") as a:
    #    a.write(data)
    pyperclip.copy(data)

def webedit(url,data):
    width,height = pyautogui.size()
    webbrowser.open(url)
    time.sleep(randrange(3,10))
    pyautogui.moveTo(width/2,height/2)
    pyautogui.click()
    pyautogui.hotkey("ctrl","a")
    if data == "clip":
        pyautogui.hotkey("ctrl","c")
        edit()
    else:
        pyperclip.copy(data)
    time.sleep(0.5)
    pyautogui.hotkey("ctrl","v")
    for r in range(randrange(7)):
        pyautogui.moveTo(randrange(width),randrange(height))
    for r in range(3):
        pyautogui.press("tab")
        time.sleep(uniform(0.2,1.5))
    pyautogui.press("space")
    time.sleep(randrange(3,10))
    pyautogui.hotkey("ctrl","w")

with open("c:/users/crazy/pictures/python/spell.txt",encoding="utf-8") as f:
    data = f.read().split("    ")
spells={}
offset = 0
for key in charList:
    length = len([j for j in charList[key] if not "\u0014" in j])
    if length == 0:
        continue
    spells[key] = []
    for i in range(length):
        if not [j for j in charList[key] if not "\u0014" in j][i] in data[offset].split("\n")[0]:
            print(charList[key][i]," error")
        spells[key].append(data[offset])
        offset+=1

if sys.argv[1] == "edit":
    edit()
elif sys.argv[1] == "spell":
    url = "https://namu.wiki/edit"
    #url = "https://namu.wiki/history"
    #url = "https://namu.wiki/w"
    for th in list(charList.keys()):
        i=0
        for char in charList[th]:
            if "\u0014" in char:
                continue
            #webedit(f"{url}/{char}/스펠카드",spells[th][i])
            webedit(f"{url}/{char}/스펠카드","clip")
            i+=1
        time.sleep(randrange(3,10))
elif sys.argv[1] == "mari":
    url = "https://namu.wiki/edit/"
    for char in grimari:
        if "\u0014" in char:
            webedit(f"{url}/{char}/작중 행적","clip")
        else:
            webedit(f"{url}/{char}","clip")
        time.sleep(randrange(3,10))
elif sys.argv[1] == "watch":
    while(True):
        for char in ["조토구 마유미","하니야스신 케이키"]:
            response = requests.get(f"https://namu.wiki/w/{char}/스펠카드")
            data = response.content.decode("utf-8")
            if "식륜" in data:
                webedit(f"https://namu.wiki/edit/{char}/스펠카드","clip")
                print(f"{datetime.datetime.now():%H:%M} - {char}")
            else:
                print(f"{datetime.datetime.now():%H:%M} - no")
        time.sleep(300)
        
"""
    url = "https://www.thpatch.net/w/index.php?title=Translations:"
    for i in range(int(sys.argv[2])):
        webbrowser.open(url+"%s/Spell_cards/%d/ko&action=edit"%(sys.argv[1],i+1))
        if (i+1)%10 == 0:
            for t in range(5):
                pyautogui.hotkey("ctrl","tab")
            input()
            pyautogui.hotkey("alt","tab")
            time.sleep(0.1)
            for t in range(10):
                pyperclip.copy("empty")
                pyautogui.press("tab")
                pyautogui.hotkey("ctrl","a")
                pyautogui.hotkey("ctrl","c")
                text = pyperclip.paste()
                if "「" in text and "」" in text:
                    if text[0] == "「":
                        text = text.replace("「","\"")
                    else:
                        text = text.replace("「"," \"")
                    text = text.replace("」","\"")
                    pyperclip.copy(text)
                    pyautogui.hotkey("ctrl","v")
                    for t2 in range(4):
                        pyautogui.press("tab")
                    pyautogui.press("space")
                    pyautogui.hotkey("ctrl","tab")
                else:
                    pyautogui.hotkey("ctrl","w")
                time.sleep(0.1)
            input()
"""