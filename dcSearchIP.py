import requests
from bs4 import BeautifulSoup 
import time

prefix = "http://gall.dcinside.com/board/lists/?id="
gallID = "touhou"
IPaddr = "125.177"
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

for code in range(1,51):
    response = requests.get(f"{prefix}{gallID}&page={code}",headers = headers)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table",class_="gall_list")
    trs = table.find_all("tr")

    for tr in trs:
        ip = tr.find("span",class_="ip")
        if ip is not None and ip.text[1:-1] == IPaddr:
            postNum = tr.find("td",class_="gall_num").text
            title = tr.find("td",class_="gall_tit ub-word").find("a").text
            nickname = tr.find("span",class_="nickname").text
            print(f"http://gall.dcinside.com/{gallID}/{postNum}  {title}  {nickname}{ip.text}")
                
    if code%10 == 0:
        print(f"searching {code}")
        
    time.sleep(1)
print("Quit")