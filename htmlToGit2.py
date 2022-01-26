import os
import sys
import shutil
import datetime
from bs4 import BeautifulSoup
from tkinter import messagebox

site = sys.argv[1]
path = "d:/touhou/doujin/"+site
gitPath = "d:/touhou/doujin/rosenrose"
nasUrl = "http://crazytempler.ipdisk.co.kr:81/publist/HDD1/Public/doujin/"+site
nasPath = "z:/doujin/"+site

def writeLog(msg):
    with open("c:/users/crazy/pictures/python/htmltogit.log","a",encoding="utf-8-sig") as a:
        a.write(msg)

def replaceSpecialCh(title):
    res = title.replace('\\', '＼')
    res = res.replace('/', '／')
    res = res.replace(':','：')
    res = res.replace('*','＊')
    res = res.replace('?','？')
    res = res.replace('\"','＂')
    res = res.replace('<','〈')
    res = res.replace('>','〉')
    res = res.replace('|','｜')
    res = res.replace('#','＃')
    return res

def getDate(date):
    if site == "ghap":
        dateTuple = datetime.datetime.strptime(date,"%Y.%m.%d %H:%M")
    elif site == "enlsparker":
        dateTuple = datetime.datetime.strptime(date,"%Y-%m-%d")
    elif site == "ruliweb":
        dateTuple = datetime.datetime.strptime(date,"%Y.%m.%d (%H:%M:%S)")
    elif site == "dcinside":
        dateTuple = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
    elif site == "sunmism":
        dateTuple = datetime.datetime.strptime(date,"%Y.%m.%d %H:%M")
    return dateTuple.strftime("%Y-%m-%d")


def htmlToGit(dirList):
    count = 0
    for dirs in dirList:
        with open("%s/%s"%(path,dirs),encoding="utf-8") as i:
            contents = i.read()
        soup = BeautifulSoup(contents,"html.parser")
        title = soup.find("title").text
        if site not in ["enlsparker","ruliweb","dcinside"]:
            category = soup.find("div",class_="category").text
        else:
            category = None
        date = getDate(soup.find("div",class_="date").text)

        code = dirs[:-5]
        print("\n"+code+" start")
        writeLog("\n"+code+" start\n")
        article = soup.find("div",class_="article")

        srcFolder = "%s/%s_%s"%(path,code,replaceSpecialCh(title).replace(".","．"))
        imgCount = len(os.listdir(srcFolder))
        images = article.find_all("img")        
        if site == "sunmism":
            for i in images:
                if i["src"].find("www16") != -1:
                    images.remove(i)

        if imgCount != len(images):
            messagebox.showinfo(code+" image error\n")
            input()
            #continue

        for img in images:
            if img["src"].find("http") == -1:
                fileName = img["src"].split("/")[-1]
                if fileName.split(".")[0] == "001":
                    firstImgName = fileName
                img["src"] = "{{ site.nasurl }}/%s/%s/%s"%(site,code,fileName)

        tagList = []
        tagDiv = soup.find("div",class_="tagTrail")
        if tagDiv is not None:
            if tagDiv.p.text == "태그: ":
                for tmp in tagDiv.find_all("li"):
                    if site == "ghap":
                        t = tmp.text.replace("캐릭터:히메","캐릭터:와카사기히메").replace("캐릭터:","캐릭터_").replace("장르:","장르_").replace("바쿠렌","뱌쿠렌")
                    tagList.append(t)
            else:
                print("%s incomplete tag"%(code))
                a = input()
                tagList = []
        else:
            tags = input(code+" tag: ").split(" ")
            for tag in tags:
                tagList.append(tag)

        textList = article.text.split("\n")
        if site == "ghap":
            for c in textList:
                if c.find("[") != 1 and c.find("]") != -1:
                    tag = c[c.find("[")+1:c.find("]")]
                    tag = tag.replace("(",",").replace(")",",").replace("（",",").replace("）",",")
                    tag = tag.replace("[",",").replace("]",",").replace("、",",")
                    tags = []
                    for tmp in tag.split(","):
                        if tmp.strip() != "":
                            tags.append(tmp.strip())
                    for t in tags:
                        if t not in tagList:
                            tagList.append(t)
                elif c.find("(") != -1 and c.find(")") != -1:
                    tag = c.replace("(",",").replace(")",",").replace("（",",").replace("）",",").replace("、",",")
                    tags = []
                    for tmp in tag.split(","):
                        if tmp.strip() != "":
                            tags.append(tmp.strip())
                    for t in tags:
                        if t not in tagList:
                            tagList.append(t)
        elif site == "sniperriflesr":
            findList = ["작가","서클","출연","출현","이벤트"]
            for find in findList:
                charSwitch = False
                for c in textList:
                    if c.find(find) != -1 or charSwitch:
                        if find == "출연" or find == "출현":
                            charSwitch = True
                        tag = c[c.find(":")+1:].strip()
                        tag = tag.replace("(",",").replace(")",",").replace("（",",").replace("）",",")
                        tag = tag.replace("[",",").replace("]",",").replace("、",",")
                        tags = []
                        for tmp in tag.split(","):
                            if tmp.strip() != "":
                                tags.append(tmp.strip())
                        for t in tags:
                            if find == "출연" or find == "출현":
                                if "캐릭터_"+t not in tagList:
                                    tagList.append("캐릭터_"+t)
                            else:
                                if t not in tagList:
                                    tagList.append(t)
                    if charSwitch and len(c) <= 1:
                        charSwitch = False
        elif site == "lilybin":
            for c in textList:
                if c.find("x") != -1:
                    for t in c.split("x"):
                        if "캐릭터_"+t not in tagList:
                            tagList.append("캐릭터_"+t)
                    tagList.append("커플링_"+c)


        if category is not None and category not in tagList:
            tagList.append(category)

        for i in range(len(tagList)):
            tagList[i] = replaceSpecialCh(tagList[i]).replace(" ","_").replace("-_","")

        another = soup.find("div",class_="another")
        if another is not None:
            links = another.find_all("a")
            if links is not None:
                for link in links:
                    if os.path.exists("%s/%s"%(path,link["href"])):
                        a = open("%s/%s"%(path,link["href"]),encoding="utf-8")
                    elif os.path.exists("%s_/%s"%(path,link["href"])):
                        a = open("%s_/%s"%(path,link["href"]),encoding="utf-8")
                    else:
                        continue
                    anotherContent = a.read()
                    a.close()
                    anotherCode = link["href"].split(".")[0]
                    anotherDate = getDate(BeautifulSoup(anotherContent,"html.parser").find("div",class_="date").text)
                    link["href"] = "/%s-%s_%s"%(anotherDate,site,anotherCode)

        for cmtClass in ["cb_module cb_fluid","cb_lstcomment","comment",
        "area_reply response-area padding-top","jb-discuss-list jb-discuss-list-comment"]:
            comment = soup.find("div",class_=cmtClass)
            if comment is not None:
                break

        #input("%s/_posts/%s-%s_%s.md\n"%(gitPath,date,site,code))
            
        with open("%s/_posts/%s-%s_%s.md"%(gitPath,date,site,code),"w",encoding="utf-8") as o:
            o.write("---\ntitle: \"%s\"\ntags: \""%(title.replace("\"","\\\"")))
            print(title)
            writeLog(title+"\n")
            for i in range(len(tagList)):
                o.write(tagList[i])

                have_tags = os.listdir(gitPath+"/_tags")
                if tagList[i]+".md" in have_tags:
                    print(tagList[i]+" pass")
                    writeLog(tagList[i]+" pass\n")
                    pass
                else:
                    with open("%s/_tags/%s.md"%(gitPath,tagList[i]),"w",encoding="utf-8") as f:
                        f.write("---\nname: \"%s\"\ntitle: \"%s\"\n---"%(tagList[i],tagList[i]))
                    print(tagList[i]+".md created")
                    writeLog(tagList[i]+".md created\n")

                if i < len(tagList)-1:
                    o.write(" ")
            o.write("\"\nimage: \"%s/%s/%s\"\n---\n"%(site,code,firstImgName))
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
                o.write("</p>\n<br/>\n")
                
        dstFolder = "%s/%s"%(nasPath,code)
        if os.path.exists(srcFolder) and not os.path.exists(dstFolder):
            print(code+" copy\n")
            shutil.copytree(srcFolder,dstFolder)
            
        count+=1
        if count%9999 == 0:
            os.chdir(gitPath)
            os.system("git add *")
            os.system("git commit -m \"upload posts\"")
            os.system("git push")
            if input("continue?: \n") == "n":
                break

dirList = []
for dirs in os.listdir(path):
    if dirs.find(".html") != -1:
        dirList.append(dirs)

mode = input("mode: ")
if mode == "all":
    htmlToGit(dirList)
elif mode == "range":
    start = int(input("start: "))
    end = int(input("end: "))
    htmlToGit(dirList[start:end+1])
elif mode == "print":
    for i in range(len(dirList)):
        print([i,dirList[i]])
else:
    for i in range(2,len(sys.argv)):
        if sys.argv[i].find('-') == -1:
            htmlToGit([sys.argv[i]+".html"])
        else:
            c1 = sys.argv[i].split('-')[0]
            c2 = sys.argv[i].split('-')[1]
            dirList = list(map(lambda arg: str(arg)+".html", range(int(c1),int(c2)+1)))
            htmlToGit(dirList)

os.chdir(gitPath)
os.system("git add *")
os.system("git commit -m \"upload posts\"")
os.system("git push")

