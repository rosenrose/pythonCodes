import subprocess
import win32api
import time
from ctypes import *

STD_OUTPUT_HANDLE = -11
class COORD(Structure):
    pass
COORD._fields_ = [("X", c_short), ("Y", c_short)]

def print_at(row, col, msg):
    handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    windll.kernel32.SetConsoleCursorPosition(handle, COORD(col, row))
    msg = msg.encode("utf-8")
    windll.kernel32.WriteConsoleA(handle, c_char_p(msg), len(msg), None, None)

data = open("temp.txt").read().splitlines()
for i in range(len(data)):
    data[i] = list(data[i])
height = len(data)
width = len(data[0])

data.insert(0,['0' for i in range(width+2)])    #가장자리를 0으로 감싼다(오류 방지)
for i in range(1,height+1):
    data[i].insert(0,'0')
    data[i].append('0')
data.append(['0' for i in range(width+2)])
height+=2
width+=2

def print_data():
    print_at(2, 0, "")
    # subprocess.run(["cls"].shell=True)
    temp = [i[1:width-1] for i in data[1:height-1]]
    for y in temp:
        for val in y:
            if val == '2':
                print("●",end="")
            elif val == '0':
                print("□",end="")
            else:
                print("×",end="")
        print("")

def move(pos,direction):
    if direction == "up":
        return pos[0],pos[1]-1
    elif direction == "right":
        return pos[0]+1,pos[1]
    elif direction == "down":
        return pos[0],pos[1]+1
    elif direction == "left":
        return pos[0]-1,pos[1]

def rotate(direction,rotate):
    if direction == "up":
        if rotate == "left":    return "left"
        elif rotate == "right": return "right"
    elif direction == "right":
        if rotate == "left":    return "up"
        elif rotate == "right": return "down"
    elif direction == "down":
        if rotate == "left":    return "right"
        elif rotate == "right": return "left"
    elif direction == "left":
        if rotate == "left":    return "down"
        elif rotate == "right": return "up"

def Square_Tracing(x,y):
    start = x,y
    pos = x-1,y
    initDirection = "right"
    direction = initDirection
    contours = []

    pos = move(pos,initDirection)
    contours.append(pos)
    while True:
        if (cell := data[pos[1]][pos[0]]) == '0':
            direction = rotate(direction,"left")
        elif cell == '1':
            direction = rotate(direction,"right")
            contours.append(pos)
        pos = move(pos,direction)
        if pos == start and direction == initDirection:
            break
    return contours

def get_p1p2p3(pos,direction):
    if direction == "up":       return data[pos[1]-1][pos[0]-1], data[pos[1]-1][pos[0]], data[pos[1]-1][pos[0]+1]
    elif direction == "right":  return data[pos[1]-1][pos[0]+1], data[pos[1]][pos[0]+1], data[pos[1]+1][pos[0]+1]
    elif direction == "down":   return data[pos[1]+1][pos[0]+1], data[pos[1]+1][pos[0]], data[pos[1]+1][pos[0]-1]
    elif direction == "left":   return data[pos[1]+1][pos[0]-1], data[pos[1]][pos[0]-1], data[pos[1]-1][pos[0]-1]

def Theo_Pavlidis_algorithm(x,y):
    start = x,y
    pos = x,y
    initDirection = "up"
    direction = initDirection
    contours = []

    contours.append(pos)
    while True:
        p1,p2,p3 = get_p1p2p3(pos,direction)
        if p1 == '1':
            pos = move(pos,direction)
            if pos == start and direction == initDirection:
                break
            direction = rotate(direction,"left")
            if pos == start and direction == initDirection:
                break
            pos = move(pos,direction)
            contours.append(pos)
        elif p2 == '1':
            pos = move(pos,direction)
            contours.append(pos)
        elif p3 == '1':
            direction = rotate(direction,"right")
            if pos == start and direction == initDirection:
                break
            pos = move(pos,direction)
            if pos == start and direction == initDirection:
                break
            direction = rotate(direction,"left")
            if pos == start and direction == initDirection:
                break
            pos = move(pos,direction)
            contours.append(pos)
        else:
            direction = rotate(direction,"right")
        if pos == start and direction == initDirection:
            break
    return contours

contours = []
count = 0
for y in range(height):
    for x in range(0,width-1):
        if data[y][x] == '0' and data[y][x+1] == '1':
            if (x+1,y) in contours:
                continue
            start = time.time()
            # contours = Square_Tracing(x,y)
            contours += Theo_Pavlidis_algorithm(x+1,y)
            count += 1
            # print(time.time()-start)
for c in contours:
    data[c[1]][c[0]] = '2'
    print_data()
print(count)