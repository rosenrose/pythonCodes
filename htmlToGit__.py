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
path = "d:/touhou/doujin/"
defaultPath = "C:/users/crazy/pictures/python"
gitPath = "c:/users/crazy/pictures/rosenrose.github.io"
tagRemoveList = [".","?","-","캐릭터_꼬마","캐릭터_","캐릭터_?","이벤트_?","이벤트_-",""]

def writeLog(msg):
    with open("c:/users/crazy/pictures/python/htmltogit.log","a",encoding="utf-8-sig") as a:
        a.write(datetime.datetime.now().strftime("%Y.%m.%d %H:%M")+" - ")
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
    return dateTuple.strftime("%Y-%m-%d")

def printCurrentTime(msg):
    print(msg+datetime.datetime.now().strftime("%H:%M"))

def printElapsedTime(pastTime):
    result = (datetime.datetime.now()-pastTime).total_seconds()
    print("elapsed time: %d:%d"%(result/60,result%60))

def gitBuild(msg):
    input("build?: ")
    printCurrentTime("\n==========\nbuild start: ")
    subprocess.run(["jekyll","build"],encoding="utf-8",cwd=gitPath)
    printCurrentTime("build finish: ")
    subprocess.run(["python","tagPagination.py"],encoding="utf-8",cwd=defaultPath)
    gitCommit(msg)

def gitCommit(msg):
    temp = datetime.datetime.now()
    subprocess.run(["git","add","*"],encoding="utf-8",cwd=gitPath)
    printCurrentTime("\n==========\nadd start: ")    
    subprocess.run(["git","add","*"],encoding="utf-8",cwd=gitPath+"/_site")
    printCurrentTime("\n==========\nadd finish: ")
    printElapsedTime(temp)

    temp = datetime.datetime.now()
    subprocess.run(["git","commit","-m",msg],encoding="utf-8",cwd=gitPath)
    printCurrentTime("\n==========\ncommit start: ")
    subprocess.run(["git","commit","-v","-m",msg],encoding="utf-8",cwd=gitPath+"/_site")
    printCurrentTime("\n==========\ncommit finish: ")
    printElapsedTime(temp)

    temp = datetime.datetime.now()
    printCurrentTime("\n==========\npush start: ")
    subprocess.run(["git","push","-v"],encoding="utf-8",cwd=gitPath+"/_site")
    printCurrentTime("\n==========\npush finish: ")
    printElapsedTime(temp)

    if sys.argv[1].find("sleep") != -1:
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
        if not os.path.exists("%s/%s/%s.html"%(path,site,code)):
            continue

        validList.append(code)
        imgJson = subprocess.check_output(["python","distributeImage.py","add",site,code],encoding="utf-8",cwd=defaultPath)
        imgJson = json.loads(imgJson)
        print("%s %s go to %s"%(site,code,imgJson["server"]))

        with open("%s/%s/%s.html"%(path,site,code),encoding="utf-8") as i:
            contents = i.read()
        soup = BeautifulSoup(contents,"html.parser")
        title = soup.find("title").text
        if site not in ["enlsparker","ruliweb","dcinside"]:
            category = soup.find("div",class_="category").text
        else:
            category = None
        date = getDate(soup.find("div",class_="date").text)

        print(site+" "+code+" start")
        writeLog("\n"+site+" "+code+" start\n")
        article = soup.find("div",class_="article")

        srcFolder = "%s/%s/%s_%s"%(path,site,code,replaceSpecialCh(title))
        imgCount = len(os.listdir(srcFolder))
        images = [i for i in article.find_all("img") if i["src"].find("www16") == -1]

        if imgCount != len(images):
            messagebox.showinfo(code+" image error\n")
            input()

        for img in images:
            for attr in list(img.attrs):
                if attr != "src":
                    del img[attr]
            if img["src"].find("http") == -1:
                fileName = img["src"].split("/")[-1]
                if fileName.split(".")[0] == "001":
                    firstImgName = fileName
                img["src"] = "%s/%s/%s/%s"%(imgJson["yml"],site,code,fileName)

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
                print("%s incomplete tag"%(code))
                tagList = []
        elif site != "sniperriflesr":
            tags = input(code+" tag: ")
            if tags != "":
                tagList = tagList + tags.split(" ")

        textList = article.text.split("\n")
        if site == "ghap" or site == "ghapgithub":
            exception = ["2028"]
            for c in textList:
                if c.find("[") != -1 and c.find("]") != -1 and code not in exception:
                    tag = c[c.find("[")+1:c.find("]")]
                    tag = tag.replace("(",",").replace(")",",").replace("（",",").replace("）",",")
                    tag = tag.replace("[",",").replace("]",",").replace("、",",")
                elif category == "합동인지" and ((c.find("(") != -1 and c.find(")") != -1) or c.find("-") != -1):
                    tag = c.replace("(",",").replace(")",",").replace("（",",").replace("）",",").replace("、",",").replace("-",",")
                tags = [i.strip() for i in tag.split(",") if i.strip() != ""]
                tagList = tagList + [i for i in tags if i not in tagList]
        elif site == "sniperriflesr":
            findList = ["작가 :","서클 :","출연 :","출현 :","이벤트 :",
                        "작가:","서클:","출연:","출현:","이벤트:"]
            for find in findList:
                charSwitch = False
                for c in textList:
                    if c.find(find) != -1 or charSwitch:
                        if find == "출연 :" or find == "출현 :" or find == "출연:" or find == "출현:":
                            charSwitch = True

                        if charSwitch and c.find(find) == -1:
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
                                if t not in tagList and t.find("추가") == -1:
                                    tagList.append(t)
                    if charSwitch and len(c) <= 1:
                        charSwitch = False
        elif site == "lilybin":
            textList = article.find_all("p")
            i=0
            while(i < len(textList)):
                if textList[i].find("img") is not None:
                    textList.remove(textList[i])
                else:
                    i+=1
            tmp = list(map(lambda arg: arg.contents,textList))
            textList = []
            for a in tmp:
                for b in a:
                    if b.find("<br") == -1:
                        textList.append(b)

            for c in textList:
                if c.find("[") != -1 and c.find("]") != -1:
                    tag = c[c.find("[")+1:c.find("]")]
                    tag = tag.replace("(",",").replace(")",",").replace("（",",").replace("）",",")
                    tag = tag.replace("[",",").replace("]",",").replace("、",",")
                    tags = [i.strip() for i in tag.split(",") if i.strip() != ""]
                    tagList = tagList + [i for i in tags if i not in tagList]
                if c.find("x") != -1:
                    for t in c.split("x"):
                        if "캐릭터_"+t.strip() not in tagList:
                            tagList.append("캐릭터_"+t.strip())
                    tagList.append("커플링_"+c.strip())
        elif site == "rumia0528":
            textList = article.find_all("p")
            i=0
            while(i < len(textList)):
                if textList[i].find("img") is not None:
                    textList.remove(textList[i])
                else:
                    i+=1
            tmp = list(map(lambda arg: arg.contents,textList))
            textList = []
            for a in tmp:
                for b in a:
                    if b.find("<br") == -1:
                        textList.append(b)

            for c in textList:
                if c.rfind("東方") != -1:
                    tag = c[:c.rfind("]",0,c.rfind("東方"))]
                    tag = tag.replace("(",",").replace(")",",").replace("（",",").replace("）",",")
                    tag = tag.replace("[",",").replace("]",",").replace("、",",")
                    tags = [i.strip() for i in tag.split(",") if i.strip() != ""]
                    tagList = tagList + [i for i in tags if i not in tagList]    

        if category is not None and category not in tagList:
            tagList.append(category)

        i=0
        while(i < len(tagList)):
            if tagList[i] in tagRemoveList or tagList[i].find("추정") != -1:
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
                    link["href"] = "/%s_%s"%(site,anotherCode)

        for cmtClass in ["cb_module cb_fluid","cb_lstcomment","comment","comments"
        "area_reply response-area padding-top","jb-discuss-list jb-discuss-list-comment"]:
            comment = soup.find("div",class_=cmtClass)
            if comment is not None:
                break

        notes = soup.find_all(text=lambda text:isinstance(text,bs4.element.Comment))
        for note in notes: note.extract()
        
        for i in tagList:
            if i+".md" in os.listdir(gitPath+"/_tags"):
                print(i+" pass")
                writeLog(i+" pass\n")
            else:
                with open("%s/_tags/%s.md"%(gitPath,i),"w",encoding="utf-8") as f:
                    f.write("---\nname: \"%s\"\ntitle: \"%s\"\n---"%(i,i))
                print(i+".md created")
                writeLog(i+".md created\n")

        with open("%s/_posts/%s-%s_%s.md"%(gitPath,date,site,code),"w",encoding="utf-8") as o:
            o.write("---\ntitle: \"%s\"\n"%(title.replace("\"","\\\"")))
            print(title)
            writeLog(title+"\n")
            o.write("tags: \"%s\"\n"%(" ".join(tagList)))
            o.write("image: \"%s/doujin/%s/%s/%s\"\n---\n"%(imgJson["url"],site,code,firstImgName))
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
                    o.write("https://enlsparker.blogspot.com/%s/%s.html"%(referDate,code))
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
            subprocess.run(["rclone","sync","-v",srcFolder,"%s/%s/%s"%(imgJson["path"],site,code)],
                encoding="utf-8",cwd="D:/install/rclone")
            print(code+" copy\n")
            
        count+=1
        if count%9999 == 0:
            gitBuild("upload posts")
            if input("continue?: \n") == "n":
                break
    return validList

if sys.argv[1].find("build") != -1:
    gitBuild(input("message: "))
elif sys.argv[1].find("commit") != -1:
    gitCommit(input("message: "))
else:
    site = sys.argv[1]
    mode = sys.argv[2]
    if mode == "add":
        validList = []
        for i in range(3,len(sys.argv)):
            if sys.argv[i].find('-') == -1:
                htmlToGit([sys.argv[i]])
                validList.append(sys.argv[i])
            else:
                c1 = sys.argv[i].split('-')[0]
                c2 = sys.argv[i].split('-')[1]
                validList.extend(htmlToGit(range(int(c1),int(c2)+1)))
        gitBuild("upload posts: "+site+" "+str(validList))
    else:
        dirList = [i[:-5] for i in glob("%s/%s/*.html"%(path,site))]
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