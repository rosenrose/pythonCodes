# import telegram
# my_token = '640340176:AAHnNPE5Tu28dzyP-NDPd88L-dpQB8ocfTM'
# bot = telegram.Bot(token = my_token)
# chat_id = bot.getUpdates()[-1].message.chat.id
# bot.sendMessage(chat_id = chat_id, text="테스트")

import re
with open("temp.txt",encoding="utf-8") as f:
    data=f.read()
a=re.split("\d{1,2}\\n",data)[1:]
b=[len(i.strip().split("\n")) for i in a if len(i)>0]

lines = ["||" for i in range(15)]
for e,episode in enumerate(a):
    lines[0] += f"<|15> {e+1}화 ||"
    titles = [i.strip() for i in episode.split("\n") if len(i.strip())>0]
    for t in range(15):
        if (e+1)%5==1 and t!=0:
            lines[t] += "<rowbgcolor=#fffffc>"
        if t==0:
            lines[t] += "<#fffffc>"
        if t<len(titles):
            lines[t] += f"{titles[t]}||"
        else:
            lines[t] += " ||"
    if (e+1)%5 == 0:
        for i in lines: print(i)
        lines = ["||" for i in range(15)]