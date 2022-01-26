import datetime
import copy

def drawCalendar(year, month):
    table = [['' for i in range(7)] for j in range(7)]
    dayList = ['일','월','화','수','목','금','토']
    monthDays = [31,0,31,30,31,30,31,31,30,31,30,31]
    title = f"{year}년 {month}월"
    
    if year%4 == 0:
        monthDays[1] = 29
        if year%100 == 0:
            monthDays[1] = 28
            if year%400 == 0:
                monthDays[1] = 29
    else:
        monthDays[1] = 28
    
    for i in range(len(table[0])):
        table[0][i] = dayList[i]
    
    startDay = (datetime.date(year,month,1).weekday()+1)%7
    dayCount = 1
    for i in range(1,len(table)):
        for j in range(startDay if i==1 else 0, len(table[i])):
            table[i][j] = dayCount
            dayCount += 1
            if dayCount > monthDays[month-1]:
                break
        else:
            continue
        break
    
    for i in range(5,7):
        if table[i][0] == '':
            del table[i]
    
    print(title)
    width = 5
    lines = (width+1)*7+1
    for i,row in enumerate(table):
        if i==0: print('-'*lines)
        for j,col in enumerate(row):
            if j==0: print('|',end='')
            print(f'{col:{width-1 if i==0 else width}}|',end='')
        print('\n'+'-'*lines)
    print('')

drawCalendar(2019,12)
# for i in range(1,13): drawCalendar(2019,i)