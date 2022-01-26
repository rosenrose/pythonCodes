import os
import sys
import shutil

folderList = sys.argv[1:]
KILO = 1024
KB = KILO
MB = KILO**2
GB = KILO**3

for folder in folderList:
    dirList = os.listdir(folder)
    size = 0
    flag = 0
    count = 0
    for i in range(len(dirList)):
        for file in os.listdir(os.path.join(folder,dirList[i])):
            size = size + os.path.getsize(os.path.join(folder,dirList[i],file))

        if (size >= 6*GB) or (i == len(dirList)-1):
            size = 0
            count+=1
            dstFolder = os.path.join(folder,f"split{count:02}")
            os.makedirs(dstFolder)
            for j in range(flag,i+1):
                shutil.move(os.path.join(folder,dirList[j]),dstFolder)
                print(f"{dirList[j]} to {dstFolder}")
            flag = i+1
