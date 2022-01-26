import requests
import time
from bs4 import BeautifulSoup
from tkinter import messagebox

url = "https://github.com/rosenrose/rosenrose.github.io/commits/master"
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

while(True):
    soup = BeautifulSoup(requests.get(url,headers=headers).text,"html.parser")
    alarms = soup.find("details",class_="commit-build-statuses details-overlay details-reset js-dropdown-details")
    status = alarms.summary["class"][0]
    print(status)
    if status != "bg-pending":
        messagebox.showinfo(status)
        #input()
        break
    time.sleep(30)