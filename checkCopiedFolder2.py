import subprocess
import signal
from bs4 import BeautifulSoup
from pathlib import Path
import sys

def replaceSpecialCh(title):
    res = title.replace('\\', '＼')
    res = res.replace('/', '／')
    res = res.replace(':','：')
    res = res.replace('*','＊')
    res = res.replace('?','？')
    res = res.replace('\"','＂')
    res = res.replace('<','〈')
    res = res.replace('>','〉')
    res = res.replace('|','｜')
    res = res.replace('.','．')
    res = res.replace('#','＃')
    return res

folder1 = Path("D:/touhou/doujin/"+sys.argv[1])
folder2 = Path("amazon:rosenrose/doujin/"+sys.argv[1])

process = subprocess.Popen(["D:/install/rclone/rclone","mount",str(folder2),"A:"])
while(not Path("A:").exists()):
    pass

result = []
for dirs in folder1.iterdir():
    if ".html" in str(dirs):
        code = str(dirs[:-5])
        content = dirs.read_text(encoding="utf-8")
        title = replaceSpecialCh(BeautifulSoup(content,"html.parser").find("title").text)
        result.append([f"{folder1}/{code}_{title}",len(list((folder1/f"{code}_{title}").iterdir())),
            f"{folder2}/{code}",len(list(Path("A:/"+code).iterdir()))])
process.send_signal(signal.CTRL_C_EVENT)

sum1=0
sum2=0
for r in result:
    sum1+=r[1]
    sum2+=r[3]
    if r[1] != r[3]:
        print(r)
print([sum1,sum2])