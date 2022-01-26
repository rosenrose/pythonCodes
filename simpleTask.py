import os
import shutil
import sys
import json
import subprocess
import datetime
import random
from bs4 import BeautifulSoup
from replaceSpecialCh import replaceSpecialCh

def decoratorFunc(originalFunc):
    def wrapperFunc(*args,**kwds):
        temp = datetime.datetime.now()
        print("\n==========\n start: "+datetime.datetime.now().strftime("%H:%M"))
        result = originalFunc(*args,**kwds)
        print("finish: "+datetime.datetime.now().strftime("%H:%M"))
        elapsed = (datetime.datetime.now()-temp).total_seconds()
        print("elapsed time: %d:%d"%(elapsed/60,elapsed%60))
        print(args[0])
        return result
    return wrapperFunc

@decoratorFunc
def func(*msg):
    print("func")

result=subprocess.check_output(["rclone","ls","amazonrosenrose:rosenrose/doujin/enlsparker/2014-01-blog-post_403"],encoding="utf-8")
fileList = [i.strip() for i in result.split("\n")[:-1]]
print(fileList)