import os
import sys
import shutil
from bs4 import BeautifulSoup

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
    res = res.replace('.','．')
    res = res.replace('#','＃')
    return res
"""
path = sys.argv[1]
lists = os.listdir(path)

numList = []
dirList = []
for i in range(len(lists)):
    ext = os.path.splitext(lists[i])[1]
    if os.path.isfile("%s/%s" %(path,lists[i])) and ext == ".html":
        num = os.path.splitext(lists[i])[0]
        numList.append(int(num))
    else:
        dirList.append(lists[i])
numList.sort()
dirList.sort()

with open("%s/split.txt" %(path),'w',encoding="utf-8") as ostream:
    for i in range(len(numList)):
        with open("%s/%s.html" %(path,numList[i]),encoding="utf-8") as istream:
            fileContent = istream.read()

        soup = BeautifulSoup(fileContent, "html.parser")

        title = soup.find("title").text

        temp = soup.find("div",class_="article").find_all("p")
        contents = []
        for p in temp:
            if p.find("img") is None:
                contents.append(p)

        tags = soup.find("div",class_="tagTrail").find_all("li")

        if i%30 == 0:
            ostream.write("==============================\n")
        ostream.write(str(numList[i])+"\n")
        ostream.write(title+"\n\n")
        for p in contents:
            ostream.write(p.text+"\n")
        ostream.write("태그\n")
        for t in tags:
            ostream.write(t.text+"\n")
        ostream.write("----------\n\n\n")

"""
"""
for i in range(len(numList)):
    with open("%s/%s.html" %(path,numList[i]),encoding="utf-8") as istream:
        fileContent = istream.read()
    soup = BeautifulSoup(fileContent, "html.parser")
    tags = soup.find("div",class_="tagTrail").find_all("li")
    touhou = False
    for tag in tags:
        if tag.text.find("동방") != -1:
            touhou = True
    if not touhou:
        print("%d not touhou"%(numList[i]))
        print(tags)
        print("="*30)
"""
"""
for i in range(len(numList)):
    if i%30 == 0:
        print("="*30)
    print("%s %s"%(numList[i],dirList[i]))
"""

for code in os.listdir("d:/touhou/doujin/rosenrose.github.io/content/ghap"):
    with open("d:/touhou/doujin/ghap/%s.html"%(code),encoding="utf-8") as a:
        content = a.read()
    soup = BeautifulSoup(content,"html.parser")
    title = replaceSpecialCh(soup.find("title").text)
    shutil.move("d:/touhou/doujin/rosenrose.github.io/content/ghap/%s"%(code),"d:/touhou/doujin/ghap/%s_%s"%(code,title))