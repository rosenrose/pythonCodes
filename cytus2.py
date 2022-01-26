import json
import re
import sys
import pyperclip
import shutil
import requests
import time
from urllib import parse
from pathlib import Path
from bs4 import BeautifulSoup
# from selenium import webdriver

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
character = {"PAFF": {"file": "paff001", "color": "#5c9,#32aa77"},
            "NEKO#ΦωΦ": {"file": "neko001", "color": "#c8a"},
            "ROBO_Head": {"file": "robo001", "color": "#8bb"},
            "Ivy": {"file": "ivy001", "color": "#c22,#dd3232"},
            "Crystal PuNK": {"file": "cherry002", "color": "#845,#bb7687"},
            "Vanessa": {"file": "vanessa001", "color": "#7cc"},
            "Ilka": {"file": "ilka001", "color": "#eee"},
            "Xenon": {"file": "xenon001", "color": "#933,#cb6666"},
            "ConneR": {"file": "conner001", "color": "#c84,#bb7732"},
            "Cherry": {"file": "cherry001","color": "#845,#bb7687"},
            "JOE": {"file": "joe001", "color": "#748,#aa76bb"},
            "Sagar": {"file": "sagar001", "color": "#c74,#bb6632"},
            "Rin": {"file": "rin001", "color": "#6c7"},
            "Bo Bo": {"file": "bobo001", "color": "#6c7"},
            "Aroma": {"file": "paff002", "color": "#5c9,#32aa77"},
            "Nora": {"file": "robo002", "color": "#8bb"},
            "Neko": {"file": "neko002", "color": "#c8a"},
            "Kizuna AI": {"file": "ai001", "color": "#f8a"},
            "Hans": {"file": "hans001", "color": "#aaa"},
            "Alice": {"file": "alice001", "color": "#864"},
            "Graff. J": {"file": "graffj001", "color": "#ca5"},
            "Miku": {"file": "miku001", "color": "#3cb,#32ccbb"},
            "Kaf": {"file": "kaf001", "color": "#34f"},
            "Amiya": {"file": "amiya001", "color": "#0cc"}}
oachars = ["PAFF","NEKO#ΦωΦ","ROBO_Head","Vanessa","Ilka","Bo Bo","Alice","Hans","Kaf","Amiya"]
            
def text():
    cat = sys.argv[1]
    path = Path(sys.argv[2])

    data = json.load(open(path,encoding="utf-8"))
    if cat == "os":
        for i in data:
            i["Contents"] = i["Contents"][3]
    elif cat == "oa":
        for i in data["Documents"]:
            i["Contents"] = i["Contents"][3]
        for i in data["Descriptions"]:
            i["Contents"] = i["Contents"][3]
    json.dump(data,open(path.with_stem(path.stem+"_"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)

    clip = pyperclip.paste().splitlines()
    size = {12: "-3", 14: "-2", 16: "-2", 18: "-1", 20: "-1", 28: "+1", 30: "+1", 32: "+2", 33: "+2", 34: "+2", 35: "+3", 36: "+3", 38: "+3", 40: "+4", 42: "+4", 46: "+4", 48: "+5", 52: "+5", 56: "+5"}
    with open(path.with_suffix(".txt"),"w",encoding="utf-8") as f:
        for i,dat in enumerate(data if cat == "os" else data["Documents"]):
            doc = dat["Names"][0]
            f.write(f"=== {doc} ===\n")
            # if i<len(clip) and doc != clip[i][clip[i].find(" ")+1:]:
            print(f"{i+1} {doc}")
            contents = dat["Contents"].replace("  "," ")
            contents = re.compile(r"^\n##").sub("",contents)
            contents = re.compile(r"##bgm=.+?\n##").sub("",contents)
            contents = re.compile(r"conversation=(.+)\n").sub(">\g<1>: ",contents)
            contents = re.compile(r"sound=.+?,(.+)").sub(">(\g<1>)",contents)
            contents = re.compile(r"image=(.+)").sub(">[[파일:cytus2_\g<1>.png]]",contents)
            contents = re.compile(r"</?i>").sub("''",contents)
            for r in re.compile(r"<size=(\d+)>").finditer(contents):
                contents = contents.replace(r[0],f"{{{{{{{size[int(r[1])]} ")
            contents = contents.replace("</size>","}}}")
            contents = contents.replace("text\n",">")
            contents = contents.replace("  "," ")
            contents = contents.replace(" \n","\n")
            contents = contents.replace("\n","\n>")
            contents = contents.replace("> ",">")
            contents = re.compile(r"\n>$",).sub("",contents)
            for r in [i for i in re.compile(r"{{{.+?}}}",re.S).findall(contents) if ">" in i]:
                contents = contents.replace(r,r.replace(">",""))
            for r in [i for i in re.compile(r"''.+?''",re.S).findall(contents) if ">" in i]:
                contents = contents.replace(r,r.replace("\n>","''\n>''"))
            contents = re.compile(r"되(가|도[^록]|버|봐|서|야|요|있|주|줘)").sub("돼\g<1>",contents)
            contents = re.compile(r"돼(겠|고|나|냐|는|니|다|어)").sub("되\g<1>",contents)
            contents = re.compile(r"([^\d])1도").sub("\g<1>하나도",contents)
            contents = contents.replace("됬","됐")
            contents = contents.replace("떄","때")
            f.write(contents.replace("##","\n"))
            if i<(len(data)-1): f.write("\n\n")

def indent(path):
    json.dump(json.load(open(path,encoding="utf-8")),open(path,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

def export():
    path = Path(sys.argv[2])
    exports = path.glob("*_export")
    for export in exports:
        contents = list(export.iterdir())
        if dat := list(export.glob("imposts*")):
            (path/"export/imposts").mkdir(parents=True,exist_ok=True)
            if txt := list(export.glob("*.txt")):
                indent(txt[0])
                shutil.move(txt[0], path/"export/imposts"/f"{dat[0].stem.replace('imposts_','')}.json")
            else:
                raise Exception(export)
        elif dat := list(export.glob("??attachments_*.dat")):
            cat,name = dat[0].stem.split("_")
            (path/"export"/cat).mkdir(parents=True,exist_ok=True)
            if png := list(export.glob("*.png")):
                for i in png:
                    shutil.move(i, path/"export"/cat/i.name.replace('attachment',name))
            else:
                raise Exception(export)
        elif dat := (list(export.glob("illustration_*.dat"))+list(export.glob("broken_illustration_*.dat"))):
            (path/"export/illustration").mkdir(parents=True,exist_ok=True)
            for png in export.glob("*.png"):
                shutil.move(png, path/"export/illustration"/f"{dat[0].stem.replace('illustration_','')}_{png.name}")
        elif list(export.glob("songdata*")):
            (path/"export/song").mkdir(parents=True,exist_ok=True)
            if wav := list(export.glob("*.wav")):
                shutil.move(wav[0], path/"export/song")
                for txt in export.glob("*.txt"):
                    indent(txt)
                    shutil.move(txt, path/f"export/song/{txt.stem}.json")
            else:
                raise Exception(export)
        elif len(dat:=list(export.glob("*.dat"))) == 1:
            (path/"export"/dat[0].stem).mkdir(parents=True,exist_ok=True)
            for i in list(export.glob("*.png"))+list(export.glob("*.txt"))+list(export.glob("*.wav")):
                try:
                    if ".srt" in i.suffixes:
                        shutil.move(i, path/"export"/dat[0].stem/f"{i.stem}.srt")
                    elif i.suffix == ".txt":
                        indent(i)
                        shutil.move(i, path/"export"/dat[0].stem/f"{i.stem}.json")
                    else:
                        shutil.move(i, path/"export"/dat[0].stem)
                except Exception as e:
                    print(e)
                    input(i)
        shutil.rmtree(str(export))
            # print(*[i.name for i in list(export.glob("*"))],sep="\n")

def msg():
    path = Path(sys.argv[2]) / sys.argv[3]

    data = json.load(open(path,encoding="utf-8"))
    msgs = [i["Contents"].replace("##json=msgs","").strip().replace("\n","\\n") for i in data if "json=msgs" in i["Contents"]]
    for i,msg in enumerate(msgs):
        # print(i)
        # if i==1:
        #     print(msg[:173],msg[173:175],msg[175:],sep="\n=====\n")
        msgs[i] = json.loads(msgs[i])
    for msg in msgs:
        for line in msg:
            if "Content" in line:
                line["Content"] = line["Content"].replace("\n","[br]")
            if "Time" in line:
                line["Time"] = line["Time"].strip()
            if (mType := line["MessageType"]) == 0:
                print(f">||<-3> {line['Content']} ||")
            elif mType == 1:
                print(f">|| || {line['Content']}|| [[파일:cytus2_{line['Avatar']}.png]][br]{line['Time']} ||")
            elif mType == 2:
                if "UserName" in line:
                    print(f">|| [[파일:cytus2_{line['Avatar']}.png]][br]{line['Time']} ||{{{{{{#710000 {line['UserName']}}}}}}}[br]{line['Content']} || ||")
                else:
                    print(f">|| [[파일:cytus2_{line['Avatar']}.png]][br]{line['Time']} ||{line['Content']} || ||")
            elif mType == 3:
                print(f">|| || [[파일:cytus2_{line['Image']}.png]]|| [[파일:cytus2_{line['Avatar']}.png]][br]{line['Time']} ||")
            elif mType == 4:
                if "UserName" in line:
                    print(f">|| [[파일:cytus2_{line['Avatar']}.png]][br]{line['Time']} ||{{{{{{#710000 {line['UserName']}}}}}}}[br][[파일:cytus2_{line['Image']}.png]] || ||")
                else:
                    print(f">|| [[파일:cytus2_{line['Avatar']}.png]][br]{line['Time']} ||[[파일:cytus2_{line['Image']}.png]] || ||")
        print("")

def rgb_to_hex(r,g,b):
    return str(hex(r))[2:]+str(hex(g))[2:]+str(hex(b))[2:]

def im_to_namu(contents):
    if contents.startswith(" "):
        contents = contents.lstrip()
    contents = contents.replace("\r\n","\n").replace("\\","\\\\")
    if result := re.compile(r">>(.+?)\n<<",re.S).search(contents):
        contents = contents.replace(result[0],result[1].replace("\n","\n>"))
    contents = contents.replace("<b>","'''").replace("</b>","'''")
    contents = contents.replace("<i>","''").replace("</i>","''")
    if result := re.compile(r"(~~)(~~)?(.*)").search(contents):
        if result[2]:
            contents = contents.replace(result[0],result[1]+result[2]+result[3].replace("~~","~\\~"))
        else:
            contents = contents.replace(result[0],result[1]+result[3].replace("~~","~\\~"))
    contents = re.compile(r"<color=(#[0-9a-fA-F]{6})[0-9a-fA-F]{2}>").sub("{{{\g<1> ",contents)
    contents = re.compile(r"<color=([^>#]+)>").sub("{{{#\g<1> ",contents).replace("</color>","}}}")
    contents = re.compile(r"되(가|도[^록]|버|봐|서|야|요|있|주|줘)").sub("돼\g<1>",contents)
    contents = re.compile(r"돼(겠|고|나|냐|는|니|다|어)").sub("되\g<1>",contents)
    contents = re.compile(r"([^\d])1도").sub("\g<1>하나도",contents)
    contents = contents.replace("됬","됐")
    contents = contents.replace("떄","때")
    return contents

def im():
    path = Path(sys.argv[2])
    locks = json.load(open(path/"im_lock_condition_data.json",encoding="utf-8"))
    topics = json.load(open(path/"im_topic_data.json",encoding="utf-8"))
    a = {i.stem.upper(): json.load(open(i,encoding="utf-8")) for i in (path/"imposts").iterdir()}
    colors = json.load(open(path/"im_avatar_data.json",encoding="utf-8"))

    # for topic in topics:
    #     if not i["Replies"]: print(i["Id"])

    sort_order = ["paff001","neko001","robo001"]
    for lock in locks:
        if len(lock["LevelLocks"]) == 1:
            lock["level"] = lock["LevelLocks"][0]["Level"]
            lock["char"] = lock["LevelLocks"][0]["SongPackId"]
        elif len(lock["LevelLocks"]) > 1:
            levels = [i["Level"] for i in lock["LevelLocks"]]
            maxLv = max(levels)
            lock["level"] = maxLv
            maxes = [i["SongPackId"] for i in lock["LevelLocks"] if i["Level"] == maxLv]
            if levels.count(maxLv) == 1:
                lock["char"] = maxes[0]
            else:
                lock["char"] = maxes[-1]
        else:
            lock["level"] = 100
            lock["char"] = "paff001"

    locks.sort(key=lambda x: (x["level"],sort_order.index(x["char"])))
    # print(*[(i["TopicId"],i["level"],i["char"]) for i in post_order],sep="\n")
    difficulty = ["EASY","HARD","CHAOS"]
    char_dict = {"paff001": "PAFF", "neko001": "NEKO", "robo001": "ROBO", "ivy001": "Ivy", "cherry002": "Crystal PuNK"}
    with open(path/"im.txt","w",encoding="utf-8") as f:
        a=set()
        # for lock in locks:
        #     for topic in topics:
        #         if topic["Id"] == lock["TopicId"]:
        #             doc = topic
        #             break
        for post in posts:
            for topic in topics:
                if topic["Id"] == post:
                    doc = topic
                    break
            a.add(doc["CharacterName"])
            for color in colors:
                if color["Id"] == doc["AvatarId"]:
                    doc["color"] = rgb_to_hex(int(color["ThemeColor"]["R"]*255),int(color["ThemeColor"]["G"]*255),int(color["ThemeColor"]["B"]*255))
                    break
            # if doc["Titles"][3].startswith("[스폰") or doc["AvatarId"].startswith("miku") or doc["AvatarId"].startswith("rayark"): continue
            f.write(" * ")
            if (not posts[doc["Id"]]["Contents"][3] and not posts[doc["Id"]]["Replies"]) or doc["Id"] == "N2601":
                f.write("(D) ")
            if lock["LevelLockDisplay"]:
                f.write("(Lv Lock) ")
            f.write("해금 조건: ")
            f.write(", ".join([f"{char_dict[i['SongPackId']]}({i['Level']+1})" for i in lock["LevelLocks"]]))
            f.write("\n ")
            if doc["UnlockCharts"]:
                f.write("해금 곡: ")
                unlocks = [i["SongId"] for i in doc["UnlockCharts"]]
                if len(set(unlocks)) == 1:
                    difficulty = ", ".join([difficulty[i["Difficulty"]] for i in doc["UnlockCharts"]])
                    f.write(f"{unlocks[0]} ({difficulty})")
                else:
                    difficulty = ", ".join([difficulty[i["Difficulty"]] for i in doc["UnlockCharts"] if i["SongId"] == unlocks[0]])
                    f.write(f"{unlocks[0]} ({difficulty})")
                    difficulty = ", ".join([difficulty[i["Difficulty"]] for i in doc["UnlockCharts"] if i["SongId"] == unlocks[1]])
                    f.write(f", {unlocks[1]} ({difficulty})")
                f.write("\n ")
            f.write(f"||<tablecolor=#dddddd><tablebgcolor=#345166><tablewidth=100%><width=10%> [[파일:cytus2_{doc['AvatarId']}.png]][br]{{{{{{#{doc['color']} {doc['CharacterName']}}}}}}} ||<width=60%>{doc['Titles'][3]} ||[[파일:cytus2_btn_like.png|width=32]] {doc['LikeCount']}||\n")
            f.write(" ||<bgcolor=#122b41><-3> {{{#!folding [ 펼치기 · 접기 ]\n")
            f.write("||<tablecolor=#dddddd><tablebgcolor=#1d2e3b><bgcolor=#345166><tablewidth=100%><-2>")
            if posts[doc["Id"]]["Attachments"]:
                f.write(f"[[파일:cytus2_{posts[doc['Id']]['Attachments'][0]}.png|width=70%]]")
                if posts[doc["Id"]]["Contents"][3]:
                    f.write("\n\n")
            if contents := posts[doc['Id']]['Contents'][3]:
                f.write(im_to_namu(contents))
            else:
                f.write(" ")
            if not contents.endswith("\n"):
                f.write("\n")
            f.write("[br] ||\n")
            if replies := posts[doc["Id"]]["Replies"]:
                for i,r in enumerate(replies):
                    a.add(r["CharacterName"])
                    reply = im_to_namu(r["Contents"][3].rstrip().replace("\n","[br]"))
                    for color in colors:
                        if color["Id"] == r["AvatarId"]:
                            r["color"] = rgb_to_hex(int(color["ThemeColor"]["R"]*255),int(color["ThemeColor"]["G"]*255),int(color["ThemeColor"]["B"]*255))
                            break
                    f.write(f"||<^|1>")
                    if i == 0:
                        f.write("<width=5%>")
                    f.write(f"[[파일:cytus2_{r['AvatarId']}.png]]||{{{{{{-2 ")
                    if r["color"] == "ffffff":
                        f.write(f"{r['CharacterName']}}}}}}}")
                    else:
                        f.write(f"{{{{{{#{r['color']} {r['CharacterName']}}}}}}}}}}}}}")
                    f.write(f"[br][br]{reply} ||\n")
            f.write("}}} ||\n")
            f.write("\n")
    # print(*[f"({i[2]}) {i[0].lstrip()}: {i[1]}" for i in sorted(a,key=lambda x: -x[2])],sep="\n")
    print(*sorted(a),sep="\n")

    # a=set()
    # for post in posts.values():
        # if not post["Contents"][3].strip() and not post["Replies"]: print(post["Id"])
        # if "\r\n" in post["Contents"][3]: print(post["Id"])
    #     a.add(post["AvatarId"])
    #     a |= set([i["AvatarId"] for i in post["Replies"]])
    # print(len(a))
    # b=set([i.stem for i in (path/"../imavatars").iterdir()])
    # print(c:=sorted(b-a),len(c))

def date():
    path = Path(sys.argv[2])
    regex = re.compile(r"(?<=_)(([\d?]{3,4}_[\d?]{2}_[\d?X]{2})(_[\w?]+)?)$")
    regex2 = re.compile(r"\[→.*?_([\d?]{3,4}_[\d?]{2}_[\d?X]{2})(_[\w?]+)?.*\]")
    regex3 = re.compile(r"\[→.*\]")
    data = {}
    c=set()
    for char in list(character.keys())[:-1]:
        osdata = json.load(open(path/f"osdata/{character[char]['file']}.json",encoding="utf-8"))
        data[char] = {}
        for os in osdata:
            if (cat:=os["Category"]) not in data[char]:
                data[char][cat] = []
            doc = {"name": (name:=os["Names"][0])}

            if result:=regex.search(name):
                # print(name,result[0],sep=f"{' '*(30-len(name))}|| ")
                doc["date"] = result[2]
            else:
                if char == "ROBO_Head" and name.startswith("Cam_Butsudou_"):
                    doc["date"] = "698_11_11"
                if char == "Xenon" and name == "Multi_File_X044":
                    doc["date"] = "696_05_10"
                else:
                    doc["date"] = "???_??_??"

            if result:=list(regex2.finditer(os["Contents"][3])):
                doc["children"] = []
                # print(set(regex3.findall(os["Contents"][3]))-set(i[0] for i in result))
                for i in result:
                    doc["children"].append({"name": i[0][2:-1], "date": i[1]})
                    # print(i[0],i[1],sep=" || ")
                if char == "ROBO_Head" and name == "Audio_Hospital_698_08_20":
                    doc["children"].append({"name": "Audio_Nora'sRoom_69̛8_̡0̧8̶_̛14̨", "date": "698_08_14"})
            data[char][cat].append(doc)
            c.add(name)
    # print(json.dumps(data,ensure_ascii=False,indent=2))
    soup = []
    a=set()
    for char in data:
        for i,cat in enumerate(data[char]):
            for j,doc in enumerate(data[char][cat]):
                anchor = f"{i+1}.{j+1}"
                if char in oachars:
                    anchor = "1."+anchor
                if not (name:=doc["name"]).startswith("Multi_File_"):
                    if char == "Kizuna AI" and j in [1,2]:
                        date = "2020_06_30"
                    elif char == "Kizuna AI" and j in range(12,17):
                        date = "687_06_30"
                    elif char == "PAFF" and (i,j)==(12,2):
                        date = "702_11_23"
                    elif char == "NEKO#ΦωΦ" and (i,j)==(9,7):
                        date = "702_11_12"
                    elif char == "Miku" and j in [5,6]:
                        date = "702_11_03~07"
                    elif char == "Hans" and j==24:
                        date = "2280_06_30"
                    elif char == "Alice" and j in [3,4,*range(6,9),*range(10,15),*range(16,26)]:
                        date = "698_05_04~09"
                    else:
                        date = doc["date"]
                    soup.append((char,anchor,name,date))
                    a.add(name)
                if "children" in doc:
                    for child in doc["children"]:
                        soup.append((char,anchor,(name,child["name"]),child["date"]))
                        # a.append((char,anchor,(name,child["name"]),child["date"]))
                else:
                    if name.startswith("Multi_"):
                        print(char, name)
    # print(*sorted(a,key=lambda x: x[0]),sep="\n")
    print(*(c-a),len(c-a),sep="\n")
    oadata = json.load(open(path/f"oasystemdata/oa_system_data.json",encoding="utf-8"))
    # for doc in oadata["Documents"]:
    #     if result:=list(regex2.finditer(doc["Contents"][3])):
    #         print(set(regex3.findall(os["Contents"][3]))-set(i[0] for i in result))
    #         for i in result:
    #             print(i[0],i[1],sep=" || ")
    for doc in oadata["Missions"]:
        char,oid,mid = doc["MissionId"].split("_")
        for c in character:
            if char == character[c]["file"]:
                char = c
                break
        oid,mid = int(oid[-1]),int(mid[-1])
        anchor = f"2.{oid+1}.{mid}"
        name = doc["Titles"][2]
        if char == "Bo Bo" and (oid,mid) == (1,1):
            date = "701_08_20"
        elif char == "Bo Bo" and (oid,mid) == (1,2):
            date = "701_10_15"
        elif char == "Bo Bo" and (oid,mid) == (1,3):
            date = "701_10_15"
        elif char == "Bo Bo" and (oid,mid) == (1,5):
            date = "701_10_20"
        elif char == "Bo Bo" and (oid,mid) == (1,6):
            date = "701_10_15"
        elif char == "Bo Bo" and (oid,mid) == (2,1):
            date = "691_04_02"
        elif char == "Bo Bo" and (oid,mid) == (2,3):
            date = "685_??_??"
        elif char == "Bo Bo" and (oid,mid) == (2,4):
            date = "701_10_22"
        elif char == "Bo Bo" and (oid,mid) == (2,5):
            date = "687_??_??"
            soup.append((char,anchor,(name,"Audio_Calder_693_10_27"),"693_10_27"))
            soup.append((char,anchor,(name,"Audio_Calder_694_05_23"),"694_05_23"))
        elif char == "Bo Bo" and (oid,mid) == (2,6):
            date = "687_06_15"
        elif char == "Bo Bo" and (oid,mid) == (3,2):
            date = "701_11_11"
        elif char == "Bo Bo" and (oid,mid) == (3,3):
            date = "701_11_03"
        elif char == "Bo Bo" and (oid,mid) == (4,1):
            date = "696_06_15"
            soup.append((char,anchor,(name,"Daisy_698_06_14"),"698_06_14"))
        elif char == "Bo Bo" and (oid,mid) == (4,2):
            date = "698_09_14"
        elif char == "Bo Bo" and (oid,mid) == (4,3):
            date = "701_10_15"
        elif char == "Bo Bo" and (oid,mid) == (4,4):
            date = "701_11_29"
        elif char == "Hans" and mid == 1:
            date = "685_05_12"
        elif char == "PAFF" and (oid,mid) == (1,1):
            date = "687_??_??"
        elif char == "PAFF" and (oid,mid) == (1,2):
            date = "688_??_??"
        elif char == "PAFF" and (oid,mid) == (1,3):
            date = "690_??_??"
        elif char == "PAFF" and (oid,mid) == (1,4):
            date = "702_12_09"
        elif char == "PAFF" and (oid,mid) == (2,1):
            date = "689_??_??"
        elif char == "PAFF" and (oid,mid) == (2,2):
            date = "691_??_??"
        elif char == "PAFF" and (oid,mid) == (2,3):
            date = "692_??_??"
        else:
            date = "???_??_??"
        # print((char,anchor,name,date))
        soup.append((char,anchor,name,date))
    # print(json.dumps(soup,ensure_ascii=False,indent=2))
    soup.sort(key=lambda x: (x[3],list(character.keys()).index(x[0]))) 
    soup = soup[14:26]+soup[:14]+soup[26:]
    # print(*soup,sep="\n")
    data = {}
    for s in soup:
        char = s[0]
        year,month,day = s[3].split("_")
        if year not in data:
            data[year] = {"length": 0, "list": {}}
        if month not in data[year]["list"]:
            data[year]["list"][month] = {"length": 0, "list": {}}
        if day not in data[year]["list"][month]["list"]:
            data[year]["list"][month]["list"][day] = {"length": 0, "list": {}}
        if char not in data[year]["list"][month]["list"][day]["list"]:
            data[year]["list"][month]["list"][day]["list"][char] = []
        data[year]["list"][month]["list"][day]["list"][char].append(s[1:3])
        data[year]["length"] += 1
        data[year]["list"][month]["length"] += 1
        data[year]["list"][month]["list"][day]["length"] += 1
    # print(json.dumps(data,ensure_ascii=False,indent=2))
    f = open(path/"oasystemdata/data.txt","w",encoding="utf-8")
    style = lambda x: f"'''{{{{{{#!html <span style=\"text-shadow: 0 0 4px #40E0D0\">{x}</span>}}}}}}'''"
    f.write(f"||<tablebordercolor=#000><tablewidth=100%><table bgcolor=#fff,#181818><rowcolor=#fff><bgcolor=#000> {style('연도')} ||<bgcolor=#111> {style('월')} ||<bgcolor=#222> {style('일')} ||<bgcolor=#333> {style('사건')} ||<bgcolor=#444> {style('캐릭터')} ||<bgcolor=#555> {style('링크')} ||\n")
    for year in data:
        if (num:=data[year]["length"]) > 1:
            f.write(f"||<|{num}> {year}년 ")
        else:
            f.write(f"|| {year}년 ")
        for month in data[year]["list"]:
            if (num:=data[year]["list"][month]["length"]) > 1:
                f.write(f"||<|{num}> {month}월 ")
            else:
                f.write(f"|| {month}월 ")
            for day in data[year]["list"][month]["list"]:
                if (num:=data[year]["list"][month]["list"][day]["length"]) > 1:
                    f.write(f"||<|{num}> {day}일 ||<|{num}> ")
                else:
                    f.write(f"|| {day}일 || ")
                for char in data[year]["list"][month]["list"][day]["list"]:
                    if (num:=len(data[year]["list"][month]["list"][day]["list"][char])) > 1:
                        f.write(f"||<|{num}><color={character[char]['color']}> {char} ")
                    else:
                        f.write(f"||<color={character[char]['color']}> {char} ")
                    for i,soup in enumerate(data[year]["list"][month]["list"][day]["list"][char]):
                        if isinstance(soup[1], str):
                            f.write(f"|| [[Cytus II/스토리/{char}#s-{soup[0]}|{soup[1]}]] ||\n")
                        else:
                            f.write(f"|| [[Cytus II/스토리/{char}#s-{soup[0]}|{soup[1][0]}[br]({soup[1][1]})]] ||\n")
    f.close()

def rank():
    namu = "https://namu.wiki"
    soup = BeautifulSoup(requests.get(parse.urljoin(namu,"LongestPages"),headers=headers).text,"html.parser")
    i = 0
    print(soup)
    while True:
        for j,doc in enumerate(soup.select_one("article > div > ul").select("li")):
            if (text:=doc.text).startswith("Cytus II"):
                print(f"{i*100+j+1}위: {text}")
        nextLink = soup.select_one("article > div > div:nth-child(2) > a:nth-child(2)")
        soup = BeautifulSoup(requests.get(parse.urljoin(namu,nextLink["href"]),headers=headers).text,"html.parser")
        i += 1
        time.sleep(1)

def compare():
    for new in Path(sys.argv[2]).glob("*00?.json"):
        old = Path(sys.argv[3]) / new.name
        if not old.exists(): continue
        # if new.read_text(encoding="utf-8") != old.read_text(encoding="utf-8"):
        #     print(new.name)
        newJson = json.loads(new.read_text(encoding="utf-8"))
        for doc in newJson:
            if (tl:="TimelineChapter") in doc: del doc[tl]
            if "Date" in doc: del doc["Date"]
        if json.dumps(newJson,ensure_ascii=False,indent=2) != old.read_text(encoding="utf-8"):
            print(new.name)

def timeline():
    path = Path(sys.argv[2])
    chapter_order = ["Architects","Decommission","cyTus","The Silence","Vanessa","The Lost","Loom","Another Me","Buried","The New World","Kizuna AI","Hans","Alice","Kaf","Graff.J","Miku","Amiya","test01","test02"]
    chapters = {}
    vers = {}
    a = []
    for char in character:
        data = json.loads((path/f"{character[char]['file']}.json").read_text(encoding="utf-8"))
        for doc in data:
            id = doc["Id"]
            chapter = doc["TimelineChapter"]["Chapter"]
            folder = doc["TimelineChapter"]["Folder"]
            index = doc["TimelineChapter"]["Index"]
            date = doc["Date"]
            cat = doc["Category"]
            a.append((char,id,doc["Names"][3],date,index))
            if not char in vers:
                vers[char] = {}
            if not cat in vers[char]:
                vers[char][cat] = []
            vers[char][cat].append((char,id,doc["Names"][3],date,index))

            if not chapter in chapters:
                chapters[chapter] = {}
            if not folder in chapters[chapter]:
                chapters[chapter][folder] = []
            chapters[chapter][folder].append((char,id,doc["Names"][3],date,index))
            # if doc["TimelineChapter"]["Chapter"] == "test01":
            #     print(char)
    for chap in chapters:
        for folder in chapters[chap]:
            chapters[chap][folder].sort(key=lambda x: x[4])
    chapters["Decommission"] = {i: chapters["Decommission"][i] for i in ["Rin","Ilka"]}
    chapters["cyTus"] = {i: chapters["cyTus"][i] for i in ["Vanessa","PAFF","NEKO","Xenon","ConneR","Cherry","JOE","Nora"]}
    chapters["The Silence"] = {i: chapters["The Silence"][i] for i in ["PAFF","NEKO","ROBO_Head","Crystal PuNK","ConneR","Sagar"]}
    chapters["Vanessa"] = {i: chapters["Vanessa"][i] for i in ["Ivy","PAFF","Rin & Sagar","ConneR","JOE"]}
    chapters["The Lost"] = {i: chapters["The Lost"][i] for i in ["Ivy & Vanessa","Main_Folder","Xenon","ConneR","Crystal PuNK"]}
    chapters["Loom"] = {i: chapters["Loom"][i] for i in ["Main_Folder","ROBO_Head","Crystal PuNK","Ivy & Vanessa"]}
    chapters["Another Me"] = {i: chapters["Another Me"][i] for i in ["ROBO_Head","Main_Folder","Crystal PuNK_1","NEKO","PAFF","Crystal PuNK_2","Ivy & Vanessa","ConneR","Sagar"]}
    chapters["Buried"] = {i: chapters["Buried"][i] for i in ["Ivy & Vanessa","Crystal PuNK","Main_Folder"]}
    chapters["test01"]["N/A"].sort(key=lambda x: x[3])
    chapters = dict(sorted(chapters.items(),key=lambda x: chapter_order.index(x[0])))
    json.dump(chapters,open(path/"timeline.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
    # print(json.dumps(vers,ensure_ascii=False,indent=2))

    anchors = {}
    cats = {}
    for char in vers:
        for i,cat in enumerate(vers[char]):
            if not cat in cats:
                cats[cat] = {}
            cats[cat][char] = vers[char][cat]
            for j,doc in enumerate(vers[char][cat]):
                id = doc[1]
                anchors[id] = f"{i+1}.{j+1}"
                if char in oachars:
                    anchors[id] = "1."+anchors[id]
    # print(json.dumps(anchors,ensure_ascii=False,indent=2))
    cats = dict(sorted(cats.items(),key=lambda x: x[0]))
    # print(json.dumps(cats,ensure_ascii=False,indent=2))

    chaper_map = {"Architects": "Chapter I. [[Operators|Architects]] (아키텍트)",
                "Decommission": "Chapter II. [[Disaster|Decommission]] (해체하다)",
                "cyTus": "Chapter III. [[Cytus(Rayark)|cyTus]] (사이터스)",
                "The Silence": "Chapter IV. [[The Silence#s-3|The Silence]] (고요)",
                "Vanessa": "Chapter V. [[Vanessa]] (바네사)",
                "The Lost": "Chapter VI. [[The Lost]] (상실)",
                "Loom": "Chapter VII. [[Loom|LOOM]] (희미함)",
                "Another Me": "Chapter VIII. [[Another Me(Rayark)|Another Me]] (또 다른 자신)",
                "Buried": "Chapter IX. [[Buried]] (매장)",
                "The New World": "Chapter X. [[The New World]] (신세계)"}
    regex = re.compile(r"(.+?)_(.+?)_(.+)")
    head = """||<tablebordercolor=#000><table bgcolor=#fff,#181818><rowcolor=#fff><bgcolor=#000> '''{{{#!html <span style="text-shadow: 0 0 4px #40E0D0">연도</span>}}}''' ||<bgcolor=#111> '''{{{#!html <span style="text-shadow: 0 0 4px #40E0D0">월</span>}}}''' ||<bgcolor=#222> '''{{{#!html <span style="text-shadow: 0 0 4px #40E0D0">일</span>}}}''' ||<bgcolor=#333> '''{{{#!html <span style="text-shadow: 0 0 4px #40E0D0">시각</span>}}}''' ||<bgcolor=#444> '''{{{#!html <span style="text-shadow: 0 0 4px #40E0D0">캐릭터</span>}}}''' ||<bgcolor=#555> '''{{{#!html <span style="text-shadow: 0 0 4px #40E0D0">링크</span>}}}''' ||"""
    with open(path/"timeline.txt","w",encoding="utf-8") as f:
        for chap in chapters:
            if chap in chaper_map:
                f.write(f"==== {chaper_map[chap]} ====\n")
            else:
                f.write(f"==== {chap} ====\n")
            for folder in chapters[chap]:
                # f.write(f"===== {folder} =====\n")
                f.write(f" * {folder}\n")
                f.write(head+"\n")
                sum = 1
                for i,doc in enumerate(chapters[chap][folder]):
                    char,id,name = doc[0],doc[1],doc[2]
                    date,time = doc[3].split("\n")
                    result = regex.match(date)
                    year,month,day = result[1],result[2],result[3]
                    
                    if sum == 1:
                        for doc_next in chapters[chap][folder][i+1:]:
                            if char == doc_next[0]:
                                sum += 1
                            else:
                                break
                        if sum > 1:
                            f.write(f"||{year} ||{month} ||{day} ||{time} ||<|{sum}> {{{{{{{character[char]['color']} {char}}}}}}} || [[Cytus II/스토리/{char}#s-{anchors[id]}|{name}]] ||\n")
                        else:
                            f.write(f"||{year} ||{month} ||{day} ||{time} || {{{{{{{character[char]['color']} {char}}}}}}} || [[Cytus II/스토리/{char}#s-{anchors[id]}|{name}]] ||\n")
                    else:
                        f.write(f"||{year} ||{month} ||{day} ||{time} || [[Cytus II/스토리/{char}#s-{anchors[id]}|{name}]] ||\n")
                        sum -= 1
                f.write("\n")
        f.write("\n\n")
        for cat in cats:
            if cat.endswith(".0"):
                f.write(f"=== {cat[0]}.x ===\n")    
            f.write(f"==== {cat} ====\n")
            f.write(head+"\n")
            for folder in cats[cat]:
                # f.write(f"===== {folder} =====\n")
                for i,doc in enumerate(cats[cat][folder]):
                    char,id,name = doc[0],doc[1],doc[2]
                    date,time = doc[3].split("\n")
                    result = regex.match(date)
                    year,month,day = result[1],result[2],result[3]
                    if i == 0:
                        f.write(f"||{year} ||{month} ||{day} ||{time} ||<|{len(cats[cat][folder])}> {{{{{{{character[folder]['color']} {folder}}}}}}} || [[Cytus II/스토리/{char}#s-{anchors[id]}|{name}]] ||\n")
                    else:
                        f.write(f"||{year} ||{month} ||{day} ||{time} || [[Cytus II/스토리/{char}#s-{anchors[id]}|{name}]] ||\n")
            f.write("\n")
    a.sort(key=lambda x: (x[3],list(character).index(x[0])))
    # for i in range(len(a)-1):
    #     if a[i][3] == a[i+1][3]: print(a[i], a[i+1])
    print(head)
    sum = 1
    for i,doc in enumerate(a):
        char,id,name = doc[0],doc[1],doc[2]
        date,time = doc[3].split("\n")
        result = regex.match(date)
        year,month,day = result[1],result[2],result[3]
        # if not re.compile(r"[\d?]{3}").match(year) or not re.compile(r"[\d?]{2}").match(month) or not re.compile(r"[\d?]{2}").match(day):
        #     print(doc)
        if sum == 1:
            for doc_next in a[i+1:]:
                if char == doc_next[0]:
                    sum += 1
                else:
                    break
            if sum > 1:
                print(f"||{year} ||{month} ||{day} ||{time} ||<|{sum}> {{{{{{{character[char]['color']} {char}}}}}}} || [[Cytus II/스토리/{char}#s-{anchors[id]}|{name}]] ||")
            else:
                print(f"||{year} ||{month} ||{day} ||{time} || {{{{{{{character[char]['color']} {char}}}}}}} || [[Cytus II/스토리/{char}#s-{anchors[id]}|{name}]] ||")
        else:
            print(f"||{year} ||{month} ||{day} ||{time} || [[Cytus II/스토리/{char}#s-{anchors[id]}|{name}]] ||")
            sum -= 1

    # print(*[" ".join([i[3].split("\n")[0],i[3].split("\n")[1],i[0],i[2]]) for i in a],sep="\n")

if __name__ == "__main__":
    if (mode:=sys.argv[1]) in ["os","oa"]:
        text()
    elif mode == "export":
        export()
    elif mode == "msg":
        msg()
    elif mode == "im":
        im()
    elif mode == "date":
        date()
    elif mode == "rank":
        rank()
    elif mode == "compare":
        compare()
    elif mode == "indent":
        indent(sys.argv[2])
    elif mode == "timeline":
        timeline()
    # else:
        # a=Path(r"D:\Obb\main.39967100.com.rayark.cytus2\3.7\bin\Data")
        # for i in a.rglob("*.png"):
        #     num=1
        #     if (a/"../png"/i.name).exists():
        #         while (a/"../png"/f"{i.stem}_{num}{i.suffix}").exists():
        #             num+=1
        #         shutil.move(i,a/"../png"/f"{i.stem}_{num}{i.suffix}")
        #     else:
        #         shutil.move(i,a/"../png")

#[^\s\wㄱ-ㅎㅏ-ㅣ가-힣ﾡ-ￜぁ-ゔァ-ヴｧ-ｳﾞﾉﾊー々〆〤ﾒゝゞヽヾ〱〲\u2e80-\u2eff\u31c0-\u31ef\u3200-\u32ff\u3400-\u4dbf\u4e00-\u9fbf\uf900-\ufaff`~!@#$%^&*()\-_=+\[\]{};:'",.<>/?\\|·『』「」《》【】（）→…⋯～»。．？！＃；：＊ŏéäüöα、—・“”∀♥♡☆★♪♫▽─≫※Æ‎ΦωД－´╥･╯╰╮╭σ╬ㄟㄏ₃ˋˊ°ㅣﾟ，＼／ㄛㄋ≡ლ｀๑•̀و•́￣͡ʖ͜▕ฅ☼〒◢◣×ﬁﬂ╹◡︿]+