import os
import sys
import shutil
import datetime
import bs4
import subprocess
import json
from bs4 import BeautifulSoup
from tkinter import messagebox
from selenium import webdriver
from replaceSpecialCh import replaceSpecialCh
from glob import glob

gitUrl = "https://github.com/rosenrose/rosenrose.github.io/commits/master"
path = "G:/doujin/"
defaultPath = "C:/users/crazy/pictures/python"
gitPath = "D:/Touhou/rosenrose.github.io"
tagRemoveList = [".","?","-","캐릭터_꼬마","캐릭터_","캐릭터_?","이벤트_?","이벤트_-",""]

def writeLog(msg):
    with open("c:/users/crazy/pictures/python/htmltogit.log","a",encoding="utf-8-sig") as a:
        a.write(f"{datetime.datetime.now():%Y.%m.%d %H:%M} - ")
        a.write(msg)

def convertTag(tag):
    res = tag.lower()
    res = res.replace(" ","_")
    res = res.replace("　","_")
    res = res.replace(" ","_")
    res = res.replace("-_","")
    res = res.replace("_／_","／")
    res = res.replace("[","")
    res = res.replace("]","")
    res = res.replace("(?)","")
    res = res.replace("이누바리시","이누바시리")
    res = res.replace("이바나","이나바")
    res = res.replace("와카사키","와카사기")
    res = res.replace("바쿠렌","뱌쿠렌")
    res = res.replace("이마이즈마","이마이즈미")
    res = res.replace("마가드로이드","마가트로이드")
    res = res.replace("레미리아","레밀리아")
    res = res.replace("메를린","메를랑")
    res = res.replace("에타니티","이터니티")
    res = res.replace("히나나에","히나나위")
    res = res.replace("타타로","타타라")
    res = res.replace("세치반키","세키반키")
    res = res.replace("헤카티라","헤카티아")
    res = res.replace("라파스라","라피스라")
    res = res.replace("쿄쿄","쿄코")
    res = res.replace("샤메미마루","샤메이마루")
    res = res.replace("샤이교우지","사이교우지")
    res = res.replace("후치와라노","후지와라노")
    res = res.replace("엘리스_마가","앨리스_마가")
    res = res.replace("미미노_후토","미미노_미코")
    res = res.replace("요이_스칼렛","요이_사쿠야")
    res = res.replace("우시마","우사미")
    res = res.replace("와사츠키노","와타츠키노")
    res = res.replace("히리지","히지리")
    res = res.replace("세키만비","세키반키")
    res = res.replace("뱌루렌","뱌쿠렌")
    res = res.replace("야큐","아큐")
    res = res.replace("메이린","메이링")
    res = res.replace("마미조우","마미조")
    res = res.replace("쇼우","쇼")
    res = res.replace("유우기","유기")
    res = res.replace("노우렛지","널릿지")
    res = res.replace("노우릿지","널릿지")
    res = res.replace("카게로우","카게로")
    res = res.replace("죠온","조온")
    res = res.replace("준코","순호")
    res = res.replace("쿄우코","쿄코")
    res = res.replace("카엔뵤우","카엔뵤")
    res = res.replace("헤카티야","헤카티아")
    return res

def ghap_changeTag(tag):
    tag = tag.replace(":","_")
    tag = tag.replace("서클_","")
    tag = tag.replace("_히메","_와카사기히메")
    return tag

def getDate(date):
    if site in ["ghap","sunmism","sniperriflesr","touhoustory","nonicname","lilybin","rumia0528","seiga22"]:
        dateTuple = datetime.datetime.strptime(date,"%Y.%m.%d %H:%M")
    elif site in ["enlsparker","ghapgithub"]:
        dateTuple = datetime.datetime.strptime(date,"%Y-%m-%d")
    elif site in ["ruliweb"]:
        dateTuple = datetime.datetime.strptime(date,"%Y.%m.%d (%H:%M:%S)")
    elif site in ["dcinside"]:
        dateTuple = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
    return f"{dateTuple:%Y-%m-%d)}"

def printElapsedTime(pastTime):
    result = (datetime.datetime.now()-pastTime).total_seconds()
    print(f"elapsed time: {result/60}:{result%60}")

"""def elapsedTime(function):
    def wrapperFunction(*args,**kws):
        temp = datetime.datetime.now()
        printCurrentTime("\n==========\n%s start: "%(args[0]))
        result = function(*args,**kws)
        printCurrentTime("\n==========\n%s finish: "%(args[0]))
        printElapsedTime(temp)
        return result
    return wrapperFunction"""

def elapsedTime(msg,function,*args,**kws):
    temp = datetime.datetime.now()
    print(f"\n==========\n{msg} start: {datetime.datetime.now():%H:%M}")
    function(*args,**kws)
    print(f"\n==========\n{msg} finish: {datetime.datetime.now():%H:%M}")
    printElapsedTime(temp)

def gitBuild(msg):
    input("build?: ")
    elapsedTime("build",subprocess.run,["jekyll","build"],cwd=gitPath,encoding="utf-8")
    elapsedTime("tag paginate",subprocess.run,["python","tagPagination.py"],cwd=defaultPath,encoding="utf-8")
    gitCommand(msg)

def gitCommand(msg):
    subprocess.run(["git","add","*"],cwd=gitPath,encoding="utf-8")
    elapsedTime("add",subprocess.run,["git","add","*"],cwd=gitPath+"/_site",encoding="utf-8")

    subprocess.run(["git","commit","-m",msg],cwd=gitPath,encoding="utf-8")
    elapsedTime("commit",subprocess.run,["git","commit","-v","-m",msg],cwd=gitPath+"/_site",encoding="utf-8")

    subprocess.run(["git","push","-v"],cwd=gitPath,encoding="utf-8")
    elapsedTime("push",subprocess.run,["git","push","-v"],cwd=gitPath+"/_site",encoding="utf-8")

    if "sleep" in sys.argv[1]:
        subprocess.run(["timeout","/t","30",">","NUL"],encoding="utf-8")
        subprocess.run(["shutdown","-h"],encoding="utf-8")
    
    driver = webdriver.Chrome("D:/Install/chromedriver.exe")
    driver.get(gitUrl)
    messagebox.showinfo("done")
    input()

def htmlToGit(dirList):
    count = 0
    validList = []
    for code in dirList:
        if not os.path.exists(f"{path}/{site}/{code}.html"):
            continue

        validList.append(code)
        imgJson = subprocess.check_output(["python","distributeImage.py","add",site,code],encoding="utf-8",cwd=defaultPath)
        imgJson = json.loads(imgJson)
        print(f"{site} {code} go to {imgJson['server']}")

        contents = open(os.path.join(path,site,f"{code}.html"),encoding="utf-8").read()
        soup = BeautifulSoup(contents,"html.parser")
        title = soup.find("title").text
        if site not in ["enlsparker","ruliweb","dcinside"]:
            category = soup.find("div",class_="category").text
        else:
            category = None
        date = getDate(soup.find("div",class_="date").text)

        print(f"{site} {code} start")
        writeLog(f"\n{site} {code} start\n")
        article = soup.find("div",class_="article")

        srcFolder = os.path.join(path,site,f"{code}_{replaceSpecialCh(title)}")
        imgCount = len(os.listdir(srcFolder))
        images = [i for i in article.find_all("img") if "www16" not in i["src"]]

        if imgCount != len(images):
            messagebox.showinfo(code+" image error\n")
            input()

        for img in images:
            for attr in list(img.attrs):
                if attr != "src":
                    del img[attr]
            if "http:" not in img["src"]:
                fileName = img["src"].split("/")[-1]
                if fileName.split(".")[0] == "001":
                    firstImgName = fileName
                img["src"] = f"{imgJson['yml']}/{site}/{code}/{fileName}"

        tagList = []
        tagDiv = soup.find("div",class_="tagTrail")
        if tagDiv is not None:
            if tagDiv.p is not None and tagDiv.p.text == "태그: ":
                for tmp in tagDiv.find_all("li"):
                    if site == "ghap" or site == "ghapgithub":
                        tagList.append(convertTag(ghap_changeTag(tmp.text).strip()))
                    else:
                        tag = tmp.text.replace("(",",").replace(")",",").replace("（",",").replace("）",",")
                        tag = tag.replace("[",",").replace("]",",").replace("、",",")
                        tags = [i.strip() for i in tag.split(",") if i.strip() != ""]
                        tagList = tagList + [i for i in tags if i not in tagList]
            else:
                print(f"{code} incomplete tag")
                tagList = []
        elif site != "sniperriflesr":
            tags = input(code+" tag: ")
            if tags != "":
                tagList = tagList + tags.split(" ")

        textList = article.text.split("\n")
        if site == "ghap" or site == "ghapgithub":
            exception = ["2028"]
            for c in textList:
                if "[" in c  and "]" in c and code not in exception:
                    tag = c[c.find("[")+1:c.find("]")]
                    tag = tag.replace("(",",").replace(")",",").replace("（",",").replace("）",",")
                    tag = tag.replace("[",",").replace("]",",").replace("、",",")
                elif category == "합동인지" and (("(" in c and ")" in c) or "-" in c):
                    tag = c.replace("(",",").replace(")",",").replace("（",",").replace("）",",").replace("、",",").replace("-",",")
                tags = [i.strip() for i in tag.split(",") if i.strip() != ""]
                tagList = tagList + [i for i in tags if i not in tagList]
        elif site == "sniperriflesr":
            findList = ["작가 :","서클 :","출연 :","출현 :","이벤트 :","작가:","서클:","출연:","출현:","이벤트:"]
            for find in findList:
                charSwitch = False
                for c in textList:
                    if find in c or charSwitch:
                        if find == "출연 :" or find == "출현 :" or find == "출연:" or find == "출현:":
                            charSwitch = True

                        if charSwitch and find not in c:
                            tag = c.strip()
                        else:
                            tag = c[c.find(find)+len(find):].strip()

                        tag = tag.replace("(",",").replace(")",",").replace("（",",").replace("）",",")
                        tag = tag.replace("[",",").replace("]",",").replace("、",",")
                        tags = [i.strip() for i in tag.split(",") if i.strip() != ""]
                        for t in tags:
                            if find == "출연 :" or find == "출현 :" or find == "출연:" or find == "출현:":
                                if "캐릭터_"+t not in tagList:
                                    tagList.append("캐릭터_"+t)
                            elif find =="이벤트 :" or find == "이벤트:":
                                if "이벤트_"+t not in tagList:
                                    tagList.append("이벤트_"+t)                            
                            else:
                                if t not in tagList and "추가" not in t:
                                    tagList.append(t)
                    if charSwitch and len(c) <= 1:
                        charSwitch = False
        elif site == "lilybin":
            textList = article.find_all("p")
            textList = [i for i in textList if i.find("img")]
            tmp = list(map(lambda arg: arg.contents,textList))
            textList = []
            for a in tmp:
                for b in a:
                    if "<br" not in b:
                        textList.append(b)

            for c in textList:
                if "[" in  c and "]" in c:
                    tag = c[c.find("[")+1:c.find("]")]
                    tag = tag.replace("(",",").replace(")",",").replace("（",",").replace("）",",")
                    tag = tag.replace("[",",").replace("]",",").replace("、",",")
                    tags = [i.strip() for i in tag.split(",") if i.strip() != ""]
                    tagList = tagList + [i for i in tags if i not in tagList]
                if "x" in c:
                    for t in c.split("x"):
                        if "캐릭터_"+t.strip() not in tagList:
                            tagList.append("캐릭터_"+t.strip())
                    tagList.append("커플링_"+c.strip())
        elif site == "rumia0528":
            textList = article.find_all("p")
            textList = [i for i in textList if i.find("img")]
            tmp = list(map(lambda arg: arg.contents,textList))
            textList = []
            for a in tmp:
                for b in a:
                    if "<br" not in b:
                        textList.append(b)

            for c in textList:
                if "東方" in c:
                    tag = c[:c.rfind("]",0,c.rfind("東方"))]
                    tag = tag.replace("(",",").replace(")",",").replace("（",",").replace("）",",")
                    tag = tag.replace("[",",").replace("]",",").replace("、",",")
                    tags = [i.strip() for i in tag.split(",") if i.strip() != ""]
                    tagList = tagList + [i for i in tags if i not in tagList]    

        if category is not None and category not in tagList:
            tagList.append(category)

        i=0
        while(i < len(tagList)):
            if tagList[i] in tagRemoveList or "추정" in tagList[i]:
                tagList.remove(tagList[i])
            else:
                tagList[i] = convertTag(replaceSpecialCh(tagList[i]))
                i+=1
            
        another = soup.find("div",class_="another")
        if another is not None:
            links = another.find_all("a")
            if links is not None:
                for link in links:
                    anotherCode = link["href"].split(".")[0]
                    link["href"] = f"/{site}_{anotherCode}"

        for cmtClass in ["cb_module cb_fluid","cb_lstcomment","comment","comments","area_reply response-area padding-top","jb-discuss-list jb-discuss-list-comment"]:
            comment = soup.find("div",class_=cmtClass)
            if comment is not None:
                break

        notes = soup.find_all(text=lambda text:isinstance(text,bs4.element.Comment))
        for note in notes: note.extract()
        
        for i in tagList:
            if f"{i}.md" in os.listdir(os.path.join(gitPath,"_tags")):
                print(f"{i} pass")
                writeLog(f"{i} pass\n")
            else:
                open(os.path.join(gitPath,"_tags",f"{i}.md"),"w",encoding="utf-8").write(f"---\nname: \"{i}\"\ntitle: \"{i}\"\n---")
                print(f"{i}.md created")
                writeLog(f"{i}.md created\n")

        with open(os.path.join(gitPath,"_posts",f"{date}-{site}_{code}.md"),"w",encoding="utf-8") as o:
            o.write("---\ntitle: \"%s\"\n" % title.replace("\"","\\\""))
            print(title)
            writeLog(title+"\n")
            o.write(f"tags: \"{' '.join(tagList)}\"\n")
            o.write(f"image: \"{imgJson['url']}/doujin/{site}/{code}/{firstImgName}\"\n---\n")
            o.write(str(article)+"<br/>\n")
            if tagDiv is not None:
                o.write(str(tagDiv)+"<br/>\n")
            if another is not None:
                o.write(str(another)+"<br/>\n")
            if comment is not None:
                o.write(str(comment)+"<br/>\n")
                
            if site != "ghap":
                o.write("\n<br/>\n<p id=\"refer\">")
                if site == "enlsparker":
                    referDate = date[:-3].replace("-","/")
                    o.write(f"https://enlsparker.blogspot.com/{referDate}/{code}.html")
                elif site == "ruliweb":
                    o.write("https://bbs.ruliweb.com/family/211/board/300545/read/"+code)
                elif site == "dcinside":
                    o.write("https://gall.dcinside.com/touhou/"+code)
                elif site == "sunmism":
                    o.write("https://www.sunmism.com/"+code)
                elif site == "ghapgithub":
                    o.write(soup.find("link",rel="canonical")["href"].replace("http","https"))
                elif site == "touhoustory":
                    o.write("https://touhoustory.tistory.com/"+code)
                elif site == "nonicname":
                    o.write("https://nonicname.tistory.com/"+code)
                elif site == "rumia0528":
                    o.write("https://rumia0528.tistory.com/"+code)
                elif site == "sniperriflesr":
                    o.write("https://blog.daum.net/sniperriflesr/"+code)
                o.write("</p>\n<br/>\n")

        if os.path.exists(srcFolder):
            subprocess.run(["rclone","sync","-P",srcFolder,f"{imgJson['path']}/{site}/{code}"],encoding="utf-8")
            print(code+" copy\n")
            
        count+=1
        if count%9999 == 0:
            gitBuild("upload posts")
            if input("continue?: \n") == "n":
                break
    return validList

if "build" in sys.argv[1]:
    gitBuild(input("message: "))
elif "commit" in sys.argv[1]:
    gitCommand(input("message: "))
else:
    site = sys.argv[1]
    mode = sys.argv[2]
    if mode == "add":
        validList = []
        for i in range(3,len(sys.argv)):
            if "-" not in sys.argv[i]:
                htmlToGit([sys.argv[i]])
                validList.append(sys.argv[i])
            else:
                c1 = sys.argv[i].split('-')[0]
                c2 = sys.argv[i].split('-')[1]
                validList.extend(htmlToGit(range(int(c1),int(c2)+1)))
        gitBuild("upload posts: "+site+" "+str(validList))
    else:
        dirList = [i[:-5] for i in os.listdir(path+"/"+site) if i.endswith(".html")]
        if mode == "all":
            htmlToGit(dirList)
            gitBuild("upload posts: "+site)
        elif mode == "range":
            start = int(input("start: "))
            end = int(input("end: "))
            htmlToGit(dirList[start:end+1])
            gitBuild("upload posts: "+site+" "+str(dirList[start:end+1]))
        elif mode == "print":
            for i,dir in enumerate(dirList):
                print([i,dir+".html"])        