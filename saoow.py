import sys
import re
import requests
import time
import datetime
import subprocess
from bs4 import BeautifulSoup
from tkinter import messagebox
from pathlib import Path
from lxml import etree

domain = "https://wp.touhougarakuta.com"
nasPath = Path("Z:")

def search(url):
    print(f"Current url: {url}")
    response = requests.get(url+"?MD")
    soup = BeautifulSoup(response.text,'html.parser')
    
    pathName = url[len(domain):]
    if not (localDir := nasPath/pathName).exist():
        localDir.mkdir(parents=True)

    rootList = soup.find('pre')
    icons = rootList.find_all('img')[2:]
    if len(icons) <=1 :
        print(f"{pathName} is empty")
        return
    links = rootList.find_all('a')[5:]

    dirList = []
    fileList = []
    for n,icon in enumerate(icons):
        if icon["alt"] == "directory":
            dirList.append(links[n]["href"])
        else:
            fileList.append(links[n].text)
    
    for child in dirList:
        search(domain+child)

    if set(fileList) <= set(localList := [str(i.name) for i in localDir.iterdir()]):
        print(f"Pass {pathName}")
    else:
        #messagebox.showinfo("new!")
        downList = [i for i in fileList if i not in localList and not i.endswith(".php")]
        for file in downList:
            print("Download "+file)
            with (localDir/file).open("wb") as f:
                while True:
                    try:
                        data = requests.get(domain+pathName+file).content
                    except Exception as ex:
                        print(ex)
                        print(type(ex))
                        time.sleep(10)
                    else:
                        break
                f.write(data)

def check(url):
    try:
        response = requests.get(url)
    except Exception as ex:
        print(ex,url)
        time.sleep(600)
    else:
        if response.url != url or response.status_code == 404:
            pass
        else:
            messagebox.showinfo("uploaded",url)
    time.sleep(1)

def removeElement(*element):
    for elem in element:
        if elem is not None:
            elem.getparent().remove(elem)

def archive(path):
    index = path / "index.html"
    data = index.read_text(encoding="utf-8")
    chapter, comic = [i.stem for i in index.parents][:2]

    data = re.compile(r"\./[^>]+_files/").sub(f"", data)
    data = re.compile(r"<style data-href=.+?>").sub("<style>", data)
    data = re.compile(r"https://s3-ap-northeast-1.amazonaws.com/touhougarakuta-statics/putfykzd/wp-content/uploads/\d+/\d+/\d+/").sub("", data)
    # data = re.compile(r"logo-1.0.0.png\" style=\"height:\s*\d+px").sub("/saoow/logo-1.0.0.png\" style=\"height:25px", data)
    data = re.compile(r"href=\"https://touhougarakuta.com/index_.+?/.+?\"").sub("href=\"..\"", data)
    data = re.compile(r"href=\"https://touhougarakuta.com/novel/youseijintyouge_\d+\"").sub("href=\"..\"", data)
    data = re.compile(r"href=\"https://touhougarakuta.com/novel/youseijintyouge_\d+/1\"").sub("href=\"1\"", data)
    data = re.compile(r"src=\"jinchoge_sashie(\d+)-\d+x\d+.(jpg|png)\"").sub("src=\"/saoow/youseijinchouge/illust_gallery/jinchoge_sashie\g<1>.\g<2>\"", data)
    data = re.compile(r"srcset=\".+?\"").sub("", data)
    data = re.compile(r"※配信期限.+?\d+:\d+").sub("", data)
    data = data.replace("https://touhougarakuta.com/static/", "/saoow/static/")
    data = re.compile(r"\"https://touhougarakuta.com/?\"").sub("\"/saoow/\"", data)
    data = re.compile(r"\"(banner-2|(footer_)?logo-1\.0\.0|(([^\"]+?_)?icon|button)[^\"]+?)(\.(png|jpg|svg))\"").sub("\"/saoow/static/\g<1>\g<5>\"", data)
    data = data.replace("\"1.png\"", "\"/saoow/banner-1.png\"")
    data = data.replace("\"1570093300351.jpg\"", "\"/saoow/youseijinchouge/1570093300351.jpg\"")
    data = data.replace("\"e9c1544d692a16930cb2fbcdf6935b61.jpg\"", "\"/saoow/youseijinchouge/e9c1544d692a16930cb2fbcdf6935b61.jpg\"")
    data = data.replace("yosei_logo_fix.jpg", "/saoow/youseijinchouge/yosei_logo_fix.jpg")
    data = data.replace("yosei_visual2.jpg", "/saoow/youseijinchouge/yosei_visual2.jpg")
    data = data.replace("【公開終了】", "")

    divRegex = re.compile(r"<div style=\"flex-direction: ?column;?\">(.+?)</div>", re.DOTALL)
    imgRegex = re.compile(r"(<img src=\")(.+?\">)", re.DOTALL)
    coverRegex = re.compile(r"(style=['\"]background-image: ?url\(\"?)(.+?\"?\);?['\"]>)", re.DOTALL)
    div = divRegex.search(data)
    img = div[1]
    newImg = imgRegex.sub(f"\g<1>https://d2l1b145ht03q6.cloudfront.net/saoow/{comic}/{chapter}/\g<2>", img)
    data = data.replace(img, newImg)
    cover = coverRegex.search(data)[0]
    newCover = coverRegex.sub(f"\g<1>https://d2l1b145ht03q6.cloudfront.net/saoow/{comic}/{chapter}/\g<2>", cover)
    data = data.replace(cover, newCover)

    xml = etree.fromstring(data, parser=etree.HTMLParser(encoding="utf-8"))
    regexpNS = "http://exslt.org/regular-expressions"
    removeElement(*xml.findall(".//script"))
    removeElement(*xml.findall(".//iframe"))
    removeElement(xml.find(".//style[@class = 'vjs-styles-defaults']"))
    removeElement(*xml.xpath("//link[re:test(@rel, 'prefetch|preload|sitemap|stylesheet')]", namespaces={"re":regexpNS}))
    removeElement(*xml.xpath("//meta[re:test(@name, 'google-site-verification|twitter:card|twitter:site|fb:app_id')]", namespaces={"re":regexpNS}))
    removeElement(*xml.xpath("//meta[re:test(@property, 'fb:app_id')]", namespaces={"re":regexpNS}))
    removeElement(*xml.xpath("//div[re:test(@class, 'background|nextArticle|discription|search|search_area|sns|banner|goog-|ReactModalPortal')]", namespaces={"re":regexpNS}))
    removeElement(*xml.xpath("//div[re:test(@id, 'goog-')]", namespaces={"re":regexpNS}))
    removeElement(*xml.xpath("//h3[contains(text(), 'おすすめ記事')]"))
    removeElement(*xml.xpath("//h3[re:test(text(), '同じカテゴリの記事|新着記事')]/..", namespaces={"re":regexpNS}))
    etree.indent(xml, space="  ")
    xml = etree.tostring(xml, encoding="utf-8", method="html", doctype="<!DOCTYPE html>")

    index.with_stem("original").write_text(index.read_text(encoding="utf-8"), encoding="utf-8")
    index.write_text(xml.decode("utf-8"), encoding="utf-8")
    subprocess.run(["rclone", "move", path.resolve(), f"amazon_rosenrose:/rosenrose/saoow/{comic}/{chapter}", "--include", "*.jpg", "-v", "-P"])

if __name__ == "__main__":
    base = Path("D:/git/saoow")
    for path in sys.argv[1:]:
        archive(base/path)
        # print(path)
        # for index in (base/path).rglob("index.html"):
        #     archive(index)
            # xml = etree.fromstring(index.read_text(encoding="utf-8"),parser=etree.HTMLParser(encoding="utf-8"))
            # removeElement(xml.find(".//meta[@name = 'google-site-verification']"))
            # removeElement(xml.find(".//meta[@name = 'twitter:card']"))
            # removeElement(xml.find(".//meta[@name = 'twitter:site']"))
            # removeElement(xml.find(".//meta[@property = 'fb:app_id']"))
            # xml = etree.tostring(xml,encoding="utf-8",method="html",doctype="<!DOCTYPE html>")
            # index.write_text(xml.decode("utf-8"),encoding="utf-8")

# while True:
#     search(domain+sys.argv[1])
#     search(domain+"/wp-content/uploads/2020/03/")

#     check(sys.argv[1])
#     print(datetime.datetime.today())
#     time.sleep(600)