import sys
import re

path = "D:/Touhou/TouhouSuperExtractor1.2.5/th06_data"
name = sys.argv[1]
file = "C:/Users/crazy/pictures/python/"

with open("%s/%s" %(path,name),encoding="utf-8-sig") as f:
    lines = f.readlines()

output=[]
for line in lines:
    """
    start = line.find("print(")
    if(start != -1):
        left = line.find('（')
        right = line.find('）')

        if left == -1:
            if right == -1:
                output.append(line[start+7:-4].strip())
            else:
                output.append(line[start+7:right].strip())
        else:
            if right == -1:
                output.append(line[left+1:-4].strip())
            else:
                output.append(line[left+1:right].strip())"""
    start = line.rfind(";")
    p = re.compile('[^0-9@\-\s]')
    if start != -1 and p.match(line[start+1]) != None:
        output.append(line[start+1:-1].strip())

with open(file+name,'w',encoding="utf-8-sig") as f:
    for o in output:
        f.write(o+"\n")
