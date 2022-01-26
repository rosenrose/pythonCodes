import urllib3
import requests
from bs4 import BeautifulSoup
import telegram
import time
from datetime import datetime
from tkinter import messagebox

codes = ["3401","2039"]
url = "https://kupis.konkuk.ac.kr/sugang/acd/cour/aply/CourInwonInq.jsp?ltYy=2018&ltShtm=B01012&sbjtId="
my_token = '640340176:AAHnNPE5Tu28dzyP-NDPd88L-dpQB8ocfTM'

while True:
    for code in codes:
        try:
            response = requests.get(url+code)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find_all('table', { 'class': 'table_bg' })[1]
            tr1 = table.find_all('tr')[1]
            tr2 = table.find_all('tr')[2]
            td0 = tr1.find_all('td')[0].text
            td1 = tr1.find_all('td')[1].text
            td2 = tr2.find_all('td')[0].text
            td3 = tr2.find_all('td')[1].text
            now = datetime.now()
            if td1 == td3:
                print(f"{now:%H:%M} - {code}{td0}{td1}{td2}{td3}")
            else:
                bot = telegram.Bot(token = my_token)
                chat_id = bot.getUpdates()[-1].message.chat.id
                bot.sendMessage(chat_id = chat_id, text=code+" 자리 났음")
                print(f"{now:%H:%M} - {code}{td0}{td1}{td2}{td3}")
                messagebox.showinfo("", code+" 자리 났음")
        except requests.exceptions.RequestException as e:
            messagebox.showinfo("", code+" 연결 불가능")
            bot = telegram.Bot(token = my_token)
            chat_id = bot.getUpdates()[-1].message.chat.id
            bot.sendMessage(chat_id = chat_id, text="연결 불가능")

    time.sleep(30)