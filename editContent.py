import os
from bs4 import BeautifulSoup
import shutil
import sys
import re

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

def convertPost():
    for post in os.listdir(folder2):
        if post.find("lilybin") == -1:
            continue

        with open(folder2+"/"+post,encoding="utf-8") as f:
            lines = f.readlines()
        content = ""
        for i in range(5, len(lines)):
            content = content+lines[i]

        soup = BeautifulSoup(content,"html.parser")

        with open(folder2+"/"+post,"w",encoding="utf-8") as f:
            for i in range(0,5):
                f.write(lines[i])
            f.write(str(soup))

folder2 = "c:/users/crazy/pictures/rosenrose.github.io/_posts"
convertPost()

"""
    imgServerSuffix = ".s3.amazonaws.com/doujin/"

    for post in os.listdir(folder2):
    #for post in ["2019-03-09-lilybin_19314.md","2019-03-09-lilybin_19193.md"]:
        with open(folder2+"/"+post,encoding="utf-8") as f:
            content = f.read()

        if post.find("ghap") != -1:
            imgUrl = "{{ site.imgserver2 }}"
            imgServer = "https://franch4569"
        elif post.find("enlsparker") != -1:
            imgUrl = "{{ site.imgserver3 }}"
            imgServer = "https://kjw4569"
        elif post.find("sunmism") != -1 or post.find("sniperriflesr") != -1 or post.find("lilybin") != -1:
            imgUrl = "{{ site.imgserver4 }}"
            imgServer = "https://franch122"
        else:
            imgUrl = "{{ site.imgserver1 }}"
            imgServer = "https://rosenrose"

        content = content.replace("{{ site.nasurl }}",imgUrl).split("\n")
        img = content[3][content[3].find("\"")+1:-1]
        content[3] = "image: \"%s\""%(imgServer+imgServerSuffix+img)

        with open(folder2+"/"+post,"w",encoding="utf-8") as f:
            for line in content:
                f.write(line+"\n")
"""

"""
    for post in os.listdir(folder2):
        with open(folder2+"/"+post,encoding="utf-8") as f:
            lines = f.readlines()

        content = ""
        for i in range(5, len(lines)):
            content = content+lines[i]

        soup = BeautifulSoup(content,"html.parser")
        another = soup.find("div",class_="another")

        if another is None:
            continue
        anothers = another.find_all("a")
        for i in range(len(anothers)):
            anothers[i]["href"] = "/"+anothers[i]["href"][12:]
            
        with open(folder2+"/"+post,"w",encoding="utf-8") as f:
            for i in range(0,5):
                f.write(lines[i])
            f.write(str(soup))
"""


"""
        comment = soup.find("div",class_="comment")
        if comment is None:
            continue

        notes = comment.find_all(class_=re.compile("nav"))
        for i in notes: i.decompose()

        notes = comment.find_all(class_=re.compile("media"))
        notes = comment.find_all(["ul","li"],class_=re.compile("media"))
        for i in range(len(notes)):
            for j in range(len(notes[i]["class"])):
                if notes[i]["class"][j].find("media") != -1:
                    del notes[i]["class"][j]
            if len(notes[i]["class"]) == 0:
                del notes[i]["class"]
"""

"""
    for post in os.listdir(folder2):
        with open(folder2+"/"+post,encoding="utf-8") as f:
            content = f.read()

        if post.find("lilybin") == -1:
            continue

        content = content.replace("{{ site.imgserver4 }}","{{ site.imgserver1 }}").split("\n")
        content[3] = content[3].replace("franch122","rosenrose")

        with open(folder2+"/"+post,"w",encoding="utf-8") as f:
            for line in content:
                f.write(line+"\n")
"""