import json
import os
import sys
import datetime
import re
import subprocess
from bs4 import BeautifulSoup
from replaceSpecialCh import replaceSpecialCh
from getFolderSize import folderSize
from glob import glob

path = "c:/users/crazy/pictures/python"
doujinPath = "d:/touhou/doujin"
postPath = "c:/users/crazy/pictures/rosenrose.github.io/_posts"
folderList = ["dcinside","enlsparker","ghap","ghapgithub","lilybin","nonicname","ruliweb","rumia0528","seiga22","sniperriflesr",
                "sunmism","touhoustory"]

def writeLog(msg):
    with open("c:/users/crazy/pictures/python/distributeImage.log","a",encoding="utf-8-sig") as a:
        a.write(f"{datetime.datetime.now():%Y.%m.%d %H:%M} - ")
        a.write(msg)

def findServer(site,code):
    with open(os.path.join(path,"imgServerDB.json"),encoding="utf-8") as f:
        jsonDic = json.load(f)
    for server in jsonDic:
        if site in jsonDic[server]["site"] and code in jsonDic[server]["site"][site]:
            return server
    return ""

def addDB(site,code):
    with open(os.path.join(path,"imgServerDB.json"),encoding="utf-8") as f:
        jsonDic = json.load(f)

    server = findServer(site,code)
    if server != "":
        writeLog(code+" alreay exists\n")
    else:
        server = "Server1"
        for i in jsonDic:
            if jsonDic[server]["serverSize"] > jsonDic[i]["serverSize"]:
                server = i

        with open(os.path.join(doujinPath,site,code),encoding="utf-8") as f:
            title = replaceSpecialCh(BeautifulSoup(f.read(),"html.parser").find("title").text)
        size = folderSize(os.path.join(doujinPath,site,f"{code}_{title}"))
        count = len(os.listdir(os.path.join(doujinPath,site,f"{code}_{title}")))

        if site not in jsonDic[server]["site"]:
            jsonDic[server]["site"][site] = {}

        jsonDic[server]["site"][site][code] = {"size":size,"count":count}
        jsonDic[server]["serverSize"] = jsonDic[server]["serverSize"] + size
        jsonDic[server]["serverCount"] = jsonDic[server]["serverCount"] + count
        writeLog(f"{site} {code} go to {server}\n")

        with open(os.path.join(path,"imgServerDB.json"),"w",encoding="utf-8") as f:
            json.dump(jsonDic,f,ensure_ascii=False,indent=4)

    print(f""" {{
        "server": "{server}",
        "path": "{jsonDic[server]["path"]}",
        "url": "{jsonDic[server]["url"]}",
        "yml": "{jsonDic[server]["yml"]}"
    }} """)

def syncPost():
    with open(os.path.join(path,"imgServerDB.json"),encoding="utf-8") as f:
        jsonDic = json.load(f)

    urlRegex = re.compile("(https://)(.+)(.s3.amazonaws.com/doujin)")
    urlRegex2 = re.compile("(https://)(.+)(.cloudfront.net)")
    ymlRegex = re.compile("(\{\{ site.imgserver).( \}\})")

    for post in os.listdir(postPath):
        name = post[11:-3]
        site = name[:name.find("_")]
        code = name[name.find("_")+1:]
        print(f"{site} {code}")

        server = findServer(site,code)
        if server == "":
            print(f"{site} {code} not found")
            input(site+code)

        print(f"{site} {code} in {server}")

        content = open(os.path.join(postPath,post),encoding="utf-8").read()
        
        matchObj = urlRegex.search(content)
        if matchObj is None and urlRegex2.search(content) is None:
            input(f"{site} {code} not match")
        if matchObj is None and urlRegex2.search(content) is not None:
            continue

        if matchObj.group()[:-7] == jsonDic[server]["url"]:
            continue

        print(f"{site}_{code}: {matchObj.group()} change to {jsonDic[server]['url']}")
        writeLog(f"{site}_{code}: {matchObj.group()} change to {jsonDic[server]['url']}")
        #content = urlRegex.sub("\g<1>%s\g<3>"%(jsonDic[server]["bucket"]),content)
        content = urlRegex.sub(jsonDic[server]["url"],content)
        
        matchObj = ymlRegex.search(content)
        if matchObj is None:
            input(site+code)

        if matchObj.group() != jsonDic[server]["yml"]:
            print(f"{site}_{code}: {matchObj.group()} change to {jsonDic[server]['yml']}")
            writeLog(f"{site}_{code}: {matchObj.group()} change to {jsonDic[server]['yml']}")        
            content = ymlRegex.sub(jsonDic[server]["yml"],content)

        open(os.path.join(postPath,post),"w",encoding="utf-8").write(content)

def syncSomePost(server):
    with open(os.path.join(path,"imgServerDB.json"),encoding="utf-8") as f:
        jsonDic = json.load(f)
    urlRegex = re.compile("(image: \")(https|http)(://.+?)/(doujin/)?")

    for site in jsonDic[server]["site"]:
        for code in jsonDic[server]["site"][site]:
            for post in os.listdir(postPath):
                if f"{site}_{code}.md" in post:
                    content = open(os.path.join(postPath,post),encoding="utf-8").read()
                    matchObj = urlRegex.search(content)
                    if matchObj is None:
                        input(f"{site} {code} not match")
                    if(matchObj.group(2)+matchObj.group(3)==jsonDic[server]["url"]):
                        continue
                    print(f"{site}_{code}: {matchObj.group()} change to {jsonDic[server]['url']}")
                    writeLog(f"{site}_{code}: {matchObj.group()} change to {jsonDic[server]['url']}")
                    content = urlRegex.sub(f"\g<1>{jsonDic[server]['url']}/",content)
                    open(os.path.join(postPath,post),"w",encoding="utf-8").write(content)
                    break


def syncServer():
    with open(os.path.join(path,"imgServerDB.json"),encoding="utf-8") as f:
        jsonDic = json.load(f)

    for server in jsonDic:
        siteList = subprocess.check_output(["rclone","lsjson",jsonDic[server]["path"]],encoding="utf-8")
        siteList = json.loads(siteList)
        for sites in siteList:
            site = sites["Path"]
            codeList = subprocess.check_output(["rclone","lsjson",f"{jsonDic[server]['path']}/{site}"],encoding="utf-8")
            codeList = json.loads(codeList)
            for codes in codeList:
                code = codes["Path"]
                if site in jsonDic[server]["site"] and code in jsonDic[server]["site"][site]:
                    continue
                dstServer = findServer(site,code)
                subprocess.run(["rclone","purge","-v",f"{jsonDic[server]['path']}/{site}/{code}"],encoding="utf-8",)
                with open(os.path.join(doujinPath,site,f"{code}.html"),encoding="utf-8") as f:
                    title = replaceSpecialCh(BeautifulSoup(f.read(),"html.parser").find("title").text)
                subprocess.run(["rclone","copy","-v",f"{doujinPath}/{site}/{code}_{title}",f"{jsonDic[dstServer]['path']}/{site}/{code}"],encoding="utf-8")

                print(f"{site} {code} in {server} move to {dstServer}")
                writeLog(f"{site} {code} in {server} move to {dstServer}")

def subDB(site,code):
    with open(os.path.join(path,"imgServerDB.json"),encoding="utf-8") as f:
        jsonDic = json.load(f)

    server = findServer(site,code)
    if server == "":
        print("not in db")
        return

    jsonDic[server]["serverSize"] = jsonDic[server]["serverSize"] - jsonDic[server]["site"][site][code]["size"]
    jsonDic[server]["serverCount"] = jsonDic[server]["serverCount"] - jsonDic[server]["site"][site][code]["count"]
    del jsonDic[server]["site"][site][code]
    print(f"delete {site} {code} in {server}")

    with open(os.path.join(path,"imgServerDB.json"),"w",encoding="utf-8") as f:
        json.dump(jsonDic,f,ensure_ascii=False,indent=4)

def checkSync():
    with open(os.path.join(path,"imgServerDB.json"),encoding="utf-8") as f:
        jsonDic = json.load(f)

    for server in jsonDic:
        for site in jsonDic[server]["site"]:
            for code in jsonDic[server]["site"][site]:
                #fileJson = subprocess.check_output(["rclone","lsjson","%s/%s/%s"%(jsonDic[server]["path"],site,code)],encoding="utf-8")
                fileList = subprocess.check_output(["rclone","ls",f"{jsonDic[server]['path']}/{site}/{code}"],encoding="utf-8")
                fileList = [i.strip() for i in fileList.split("\n")[:-1]]
                sSize = 0
                sCount = len(fileList)
                for file in fileList:
                    sSize = sSize + int(file.split(" ")[0])

                dSize = jsonDic[server]["site"][site][code]["size"]
                dCount = jsonDic[server]["site"][site][code]["count"]
                if sSize != dSize or sCount != dCount:
                    writeLog(server+" "+site+" "+code+" error\n")
                    writeLog(f"sSize: {sSize}, dSize: {dSize} / sCount: {sCount}, dCount: {dCount}\n")
                    with open(os.path.join(doujinPath,site,f"{code}.html"),encoding="utf-8") as f:
                        title = replaceSpecialCh(BeautifulSoup(f.read(),"html.parser").find("title").text)
                    subprocess.run(["rclone","copy","-v",f"{doujinPath}/{site}/{code}_{title}",f"{jsonDic[server]['path']}/{site}/{code}"],encoding="utf-8")
    for server in jsonDic:
        fileList = subprocess.check_output(["rclone","ls",jsonDic[server]["path"]],encoding="utf-8")
        fileList = [i.strip() for i in fileList.split("\n")[:-1]]
        serverSize = 0
        serverCount = len(fileList)
        for file in fileList:
            serverSize = serverSize + int(file.split(" ")[0])
        if serverSize != jsonDic[server]["serverSize"] or serverCount != jsonDic[server]["serverCount"]:
            writeLog(server+" error\n")
            writeLog(f"sSize: {serverSize}, dSize: {jsonDic[server]['serverSize']} / sCount: {serverCount}, dCount: {jsonDic[server]['serverCount']}\n")

if sys.argv[1] == "add":
    addDB(sys.argv[2],sys.argv[3])
elif sys.argv[1] == "addfolder":
    for code in [i for i in os.listdir(sys.argv[2]) if os.path.isdir(os.path.join(sys.argv[2],i))]:
        #addDB(sys.argv[2],code)
        print(code)
elif sys.argv[1] == "del":
    subDB(sys.argv[2],sys.argv[3])
elif sys.argv[1] == "find":
    print(findServer(sys.argv[2],sys.argv[3]))
elif sys.argv[1] == "syncpost":
    syncPost()
elif sys.argv[1] == "syncsomepost":
    syncSomePost(sys.argv[2])
elif sys.argv[1] == "syncserver":
    syncServer()
elif sys.argv[1] == "check":
    checkSync()
elif sys.argv[1] == "addall":
    for site in folderList:
        for code in [i[:-5] for i in os.listdir(os.path.join(doujinPath,+site)) if i.find("html")!=-1]:
            addDB(site,code)
