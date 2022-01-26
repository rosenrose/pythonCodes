import subprocess
import win32api
import random
from ctypes import *

STD_OUTPUT_HANDLE = -11
class COORD(Structure):
    pass
COORD._fields_ = [("X", c_short), ("Y", c_short)]

def print_at(r, c, s):
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(h, COORD(c, r))
    s = s.encode("utf-8")
    windll.kernel32.WriteConsoleA(h, c_char_p(s), len(s), None, None)

data = open("temp.txt").read().splitlines()
for i in range(len(data)):
    data[i] = list(data[i])
height = len(data)
width = len(data[0])
marked = [[False for i in range(width)] for j in range(height)]

def print_data():
    print_at(2, 0, "")
    # subprocess.run(["cls"],shell=True)
    for y in data:
        for val in y:
            if val == '2':
                print("■",end="")
            elif val == '0':
                print("□",end="")
            else:
                print("×",end="")
        print("")

def func(x,y,count):
    queue = []
    queue.insert(0,(x,y))
    marked[y][x] = True

    while queue:
        count+=1
        i,j = queue.pop()
        if data[j][i] == '1':
            data[j][i] = '2'
            print_data()
        # print(i,j)
        adjacent = [(i,max([j-2,0])),(min([i+2,width-1]),j),
                    (i,min([j+2,height-1])),(max([i-2,0]),j)]
        # random.shuffle(adjacent)
        for ad in adjacent:
            if marked[ad[1]][ad[0]] or data[ad[1]][ad[0]] == '0':
                continue
            queue.insert(0,ad)
            # queue.append(ad)
            marked[ad[1]][ad[0]] = True
    return count

count = 0
for y in range(0,height,10):
    for x in range(0,width,10):
        if marked[y][x]:
            continue
        if data[y][x] == '1':
            count = func(x,y,count)
        else:
            marked[y][x] = True
            count+=1
print(f"count({count}) = {width}*{height}({width*height})")
subprocess.run(["cls"],shell=True)