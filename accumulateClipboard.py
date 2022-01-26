import pyperclip
import time

init = True
while True:
    if init:
        pyperclip.copy(data:="")
        init = False
    if data != (new:=pyperclip.paste()):
        pyperclip.copy(data:=data+new+"\n")
    time.sleep(0.1)