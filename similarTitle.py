import os
import sys
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

path = "D:/touhou/doujin"
searchList = ["dcinside",
"enlsparker",
"ghap",
"ghap2",
"lilybin",
"nonicname",
"ruliweb",
"rumia0528",
"seiga22",
"sniperriflesr",
"sunmism",
"touhoustory"
]

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

result = []
for search in searchList:
    lists = os.listdir("%s/%s"%(path,search))
    for i in lists:
        if os.path.isfile("%s/%s/%s" %(path,search,i)) and i.find("html") != -1:
            with open("%s/%s/%s" %(path,search,i),encoding="utf-8") as istream:
                title = BeautifulSoup(istream.read(),"html.parser").find("title").text
            code = i.split(".")[0]            
            result.append([title,search,code])

result = sorted(result,key=lambda arg: arg[0])
"""for r in result:
    print(r)"""
f = open(path+"/similar.txt","w",encoding="utf-8")
count = 0
i = 0
while(i < len(result)-1):
    if SequenceMatcher(None,result[i][0],result[i+1][0]).ratio() >= 0.95:
        count+=1
        sizes = []

        folder = "%s/%s/%s_%s"%(path,result[i][1],result[i][2],replaceSpecialCh(result[i][0]))
        sizes.append(sum(os.path.getsize("%s/%s"%(folder,f)) for f in os.listdir(folder)))

        j = i+1
        while(SequenceMatcher(None,result[i][0],result[j][0]).ratio() >= 0.95):
            folder = "%s/%s/%s_%s"%(path,result[j][1],result[j][2],replaceSpecialCh(result[j][0]))
            sizes.append(sum(os.path.getsize("%s/%s"%(folder,f)) for f in os.listdir(folder)))
            j+=1

        f.write(str(count)+"\n")
        for s in range(len(sizes)):
            f.write("%s - size: %.1f MB (%d)\n" %(result[i+s],sizes[s]/(1024*1024),sizes[s]))
        f.write("\n")
        i=j
        j+=1
    else:
        i+=1
f.close()