import urllib.request
import requests
import os
from bs4 import BeautifulSoup 

prefix = "http://gall.dcinside.com/board/view/?id=touhou&no="
prefix_ = "http://m.dcinside.com/view.php?id=touhou&no="
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
path = "D:/Touhou/remilia"

with open ("%s/remilia.txt" %(path),encoding="utf-8") as f1:
    lines = f1.readlines()

for i in range(len(lines)):
    if i%2 == 0:
        line = lines[i].split(" ")
        code = line[len(line)-1].strip()
        tmp=""
        for j in range(len(line)-1):
            tmp += (line[j]+" ")
        tmp = tmp.strip()
        food = tmp

        response = requests.get(prefix+code, headers = headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find('div', { 'class':'s_write' })
        images = div.find_all('img', { 'class':'txc-image' })

        dirname = "%s %s" % (code, food)
        if not os.path.isdir("%s/%s" % (path, dirname)):
            os.mkdir("%s/%s" % (path, dirname))

        for j in range(len(images)):
            imgUrl = images[j].get('onclick').split('\'')[1]
            imgUrl = imgUrl.replace("Pop","")
            urllib.request.urlretrieve(imgUrl, '%s/%s/%02d.png' % (path, dirname, j+1))