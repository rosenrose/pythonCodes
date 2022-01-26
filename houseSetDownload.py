import urllib.request
import requests
import re
import sys
from bs4 import BeautifulSoup 

url = sys.argv[1]
folder = sys.argv[2]
path = f"D:/Touhou/Houset set of/{folder}"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# response = requests.get("https://booth.pm/downloadables/784671?type=flac")
# soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)
table = soup.find('div',class_='variation-cart-tracks')
items = table.find_all('div',class_='download-file')
for item in items:
    name = item.find('div',class_='download-file-name').text
    if (first:=name.find(' - ')) > 0:
        name = name[:first]
    else:
        name = name[:name.find(',')]
    link = item.find('a',class_='nav-reverse free-download')['href']
    urllib.request.urlretrieve(link,f"{path}/{name}.flac")
    print(name,"   ",link)