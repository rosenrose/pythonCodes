import os
import sys
import re
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

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

def convertTag(tag):
    tag = tag.replace(":","_")
    tag = tag.replace("서클_","")
    tag = tag.replace("_히메","_와카사기히메")
    tag = tag.replace("카게로우","카게로")
    return tag

gitPath = "D:/touhou/doujin/ghapbackup.github.io/2019"
ghapPath = "D:/touhou/doujin/ghap"
tagPath = "D:/touhou/doujin/rosenrose.github.io/_tags"
catRegex = re.compile('(동방)')

with open(ghapPath+"/title.txt",encoding="utf-8") as f:
    oriTitleList = f.read().split("\n")
with open(gitPath+"/title.txt",encoding="utf-8") as f:
    titleList = f.read().split("\n")

if len(sys.argv) < 2:
    search = gitPath
else:
    search = gitPath+"/"+sys.argv[1]

for (path,dirs,files) in os.walk(search):
    for file in files:
        with open("%s/%s"%(path,file),encoding="utf-8") as f:
            content = f.read()
        soup = BeautifulSoup(content,"html.parser")
        category = soup.find("h1",class_="header")
        if category is None:
            continue
        category = category.find("a",class_="page-title-link")
        if category is None:
            continue
        category = category.text
        if not (catRegex.match(category)):
            print("out of category: "+category)
            continue
        
        title = soup.find("h1",class_="article-title").text.strip()
        
        if title in titleList:
            print("pass: "+title)
            continue
        else:
            with open(gitPath+"/title.txt","a",encoding="utf-8") as f:
                f.write(title+"\n")

        exist = False
        for t in oriTitleList:
            oriTitle = t[t.find("_")+1:]
            if SequenceMatcher(None,title,oriTitle).ratio() >= 0.95:
                exist = True
                break

        if not exist:
            print("new: "+title)
            input()
            os.system("python touhoubackup/ghap2.py \"%s/%s\""%(path,file))
            continue
        else:
            print("\ncheck tag: "+title)

        tagDiv = soup.find("div",class_="article-tag")
        if tagDiv is None:
            continue
        tagList = []
        if tagDiv.find_all("a") is not None:
            for t in tagDiv.find_all("a"):
                tagList.append(replaceSpecialCh(convertTag(t.text)))

        for oriTitles in oriTitleList:
            split = oriTitles.find("_")
            code = oriTitles[:split]
            oriTitle = oriTitles[split+1:]
            if SequenceMatcher(None,title,oriTitle).ratio() >= 0.95:
                print(code+"_"+title)
                for t in tagList:
                    print(t+" ",end="")
                print("")

                have_tags = os.listdir(tagPath)
                for tag in tagList:
                    if tag+".md" in have_tags:
                        print(tag+" pass")
                    else:
                        '''with open("%s/%s.md"%(tagPath,tag),"w",encoding="utf-8") as f:
                            f.write("---\nname: \"%s\"\ntitle: \"%s\"\n---"%(tag,tag))'''
                        print("**********new: "+tag)
                input()