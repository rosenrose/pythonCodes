import sys
import json

path = "db.json"
INTERVAL = 5000
COLWIDTH = 12

numList = json.load(open(path,encoding="utf-8"))
data = {}
for i in range(6):
    down,up = (INTERVAL*i)+1, INTERVAL*(i+1)
    data[f"{down}~{up}"] = [j for j in numList if j in range(down, up+1)]

def printHead():
    print("||",end="")
    print("="*((COLWIDTH+3)*len(data.keys())-2),end="")
    print("||")
    print("||",end="")
    for col in data:
        print(f"{col:>{COLWIDTH}} ||",end="")
    print("")
    print("||",end="")
    for col in data:
        print(f"{'='*(COLWIDTH+1)}||",end="")
    print("")

def isKeyIndex(key, index):
    for k,i,_ in keyIndex:
        if key == k and index == i:
            return True
    return False

if (mode:=sys.argv[1]) == "input":
    while True:
        numbers = [int(i) for i in input("number: ").split(" ")]
        keyIndex = []
        temp = dict(data)
        for num in numbers:
            sig = (num - 1) // INTERVAL
            key = list(data.keys())[sig]
            data[key].append(num)
            data[key].sort()
        maxlen = max([len(data[i]) for i in data])
        for num in numbers:
            sig = (num - 1) // INTERVAL
            key = list(data.keys())[sig]
            index = data[key].index(num)
            keyIndex.append((key,index,range(max(0, index-1), min(index+4, maxlen))))

        printHead()
        ranges = set()
        for r in [i[2] for i in keyIndex]:
            ranges |= set(r)
        ranges = sorted(list(ranges))
        for row in ranges:
            print("||",end="")
            for col in data:
                if row < len(data[col]):
                    if isKeyIndex(col,row):
                        current = f"*{data[col][row]}"
                        print(f"{current:>{COLWIDTH}} ||",end="")
                    elif isKeyIndex(col,row-1):
                        next = f"-->{data[col][row]}"
                        print(f"{next:>{COLWIDTH}} ||",end="")
                    elif isKeyIndex(col,row+1) or isKeyIndex(col,row-2) or isKeyIndex(col,row-3):
                        print(f"{data[col][row]:>{COLWIDTH}} ||",end="")
                    else:
                        print(f"{'':>{COLWIDTH}} ||",end="")
                else:
                    print(f"{'-':>{COLWIDTH}} ||",end="")
            print("")
        
        if (confirm := input("confirm? ")) != "":
            data = dict(temp)
        else:
            print("saved")
            numList = []
            for i in data:
                numList = [*numList, *data[i]]
            json.dump(numList,open(path,"w",encoding="utf-8"))
        print("-"*((COLWIDTH+3)*len(data.keys())+2))

elif mode == "print":
    printHead()
    maxlen = max([len(data[i]) for i in data])
    for row in range(maxlen):
        print("||",end="")
        for col in data:
            if row < len(data[col]):
                print(f"{data[col][row]:>{COLWIDTH}} ||",end="")
            else:
                print(f"{'':>{COLWIDTH}} ||",end="")
        print("")
    print("||",end="")
    print("="*((COLWIDTH+3)*len(data.keys())-2),end="")
    print("||")