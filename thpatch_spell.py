import urllib.request
import requests
import re
import sys
import openpyxl
from bs4 import BeautifulSoup 

game = sys.argv[1]
url = f"https://www.thpatch.net/w/index.php?title=Special:Translate&group=page-{game}%2FSpell+cards&task=view&language=ko"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table',class_="mw-sp-translate-table")
trs = table.find_all('tr')[3:]
if game == "Th08":
    trs = [tr for i,tr in enumerate(trs) if i%2==0]

for i,tr in enumerate(trs):
    tds = tr.find_all('td')
    # print(tds[1].text)
    print(tds[1].text[:tds[1].text.find('「')])
# for i,tr in enumerate(trs):
#     tds = tr.find_all('td')
#     result = tds[2].text[:tds[2].text.find('"')]
#     print(result.strip())
# for i,tr in enumerate(trs):
#     tds = tr.find_all('td')
#     result = tds[2].text[tds[2].text.find('"'):]
#     print(result.strip())

# wb = openpyxl.load_workbook("d:/touhou/spell cards.xlsx")
# ws = wb.worksheets[0]
# result = [text for i in list(ws.columns)[4][1:] if (text:=i.value) and (text[0] != '=')]
# for i,r in enumerate(result):
#     print(i,r)

# resultSet = set(result)
# for r in resultSet:
#     if (num := result.count(r)) > 1:
#         print(r,num)