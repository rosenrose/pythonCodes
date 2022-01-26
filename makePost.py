import os
import sys
import shutil
import datetime
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
    res = res.replace('#','＃')
    return res

site = input("site: ")
path = "d:/touhou/doujin/"+site
gitPath = "d:/touhou/doujin/rosenrose.github.io"
nasUrl = "http://crazytempler.ipdisk.co.kr:81/publist/HDD1/Public/doujin/"+site
nasPath = "z:/doujin/"+site

code = input("code: ")
title = input("title: ")
tags = input("tag: ")
date = input("date: ")
refer = input("refer: ")

tagList = []
tags = tags.split(" ")
for tag in tags:
    tagList.append(replaceSpecialCh(tag))

with open("%s/_posts/%s-%s_%s.md"%(gitPath,date,site,code),"w",encoding="utf-8") as o:
    o.write("---\ntitle: \"%s\"\ntags: "%(title))
    for i in range(len(tagList)):
        o.write(tagList[i])

        have_tags = os.listdir(gitPath+"/_tags")
        if tagList[i]+".md" in have_tags:
            pass
        else:
            with open("%s/_tags/%s.md"%(gitPath,tagList[i]),"w",encoding="utf-8") as f:
                f.write("---\nname: \"%s\"\ntitle: \"%s\"\n---"%(tagList[i],tagList[i]))
        if i < len(tagList)-1:
            o.write(" ")
    imgFiles = os.listdir("%s/%s_%s"%(path,code,replaceSpecialCh(title)))
    o.write("\nimage: %s/%s/%s\n---\n"%(site,code,imgFiles[0]))
    for imgFile in imgFiles:
        o.write("<img src=\"{{ site.nasurl }}/%s/%s/%s\"/>\n"%(site,code,imgFile))
    o.write("<br/>\n<p id=\"refer\">%s</p>"%(refer))

print(code+" copy")
shutil.copytree("%s/%s_%s"%(path,code,replaceSpecialCh(title)),"%s/%s"%(nasPath,code))

os.chdir("d:/touhou/doujin/rosenrose.github.io")
os.system("git add *")
os.system("git commit -m \"upload posts\"")
os.system("git push")