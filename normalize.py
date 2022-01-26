import os
import re
import sys
from bs4 import BeautifulSoup
import bs4

path = "d:/touhou/doujin/sniperriflesr"

for file in os.listdir(path):
    if file.find(".html") != -1:
        with open("%s/%s"%(path,file),encoding="utf-8") as i:
            contents = i.read()
        soup = BeautifulSoup(contents,"html.parser")
        article = soup.find("div",class_="article")
        spans = article.find_all("span")
        """
        for s in spans:
            if s.has_attr("style") and s["style"] == "":
                tmp = ""
                for attr in s["style"].split(";"):
                    if attr.find("COLOR") == -1 and attr != "":
                        tmp = tmp + attr + "; "
                s["style"] = tmp
            if s.has_attr("style") and s["style"] == "":
                s.unwrap()
        """
        comment = soup.find("div",class_="opinionListBox")
        if comment is not None:
            comment["class"] = "comment"
        for i in comment.find_all("input",type="hidden"):
            i.decompose()
        
        notes = soup.find_all(text=lambda text:isinstance(text,bs4.element.Comment))
        for note in notes: note.extract()
        with open("%s/%s"%(path,file),"w",encoding="utf-8") as o:
            o.write(str(soup))
        print("writing %s"%(file))