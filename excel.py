import win32com.client
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
wb = excel.Workbooks.Open("C:/Users/crazy/Dropbox/수업/18-2_전산수학/고속도로 구간거리표.xls")

def function(sheet,x1,x2,y,strXY,type):
    ws = wb.WorkSheets(sheet)
    print("// "+ws.Cells(strXY[1],strXY[0]).Value)
    j=y
    for i in range(x1,x2+1):
        if type == "A":
            #print("graph.addWeightedEdge(str1:\"%s\", str2:\"%s\", weight: %.2f);"%(ws.Cells(j-1,i).Value,ws.Cells(j,i+1).Value,ws.Cells(j,i).Value))
            s.add(ws.Cells(j-1,i).Value)
            l.append(ws.Cells(j-1,i).Value)
        else:
            #print("graph.addWeightedEdge(str1:\"%s\", str2:\"%s\", weight: %.2f);"%(ws.Cells(j,i-1).Value,ws.Cells(j+1,i).Value,ws.Cells(j,i).Value))
            s.add(ws.Cells(j,i-1).Value)
            l.append(ws.Cells(j,i-1).Value)
        j+=1

    if type == "A":
        s.add(ws.Cells(j-1,x2+1).Value)
        l.append(ws.Cells(j-1,x2+1).Value)
    else:
        s.add(ws.Cells(j,x2).Value)
        l.append(ws.Cells(j,x2).Value)
    #print("")

s = set()
l = []
function("1",2,52,5,[1,1],"A")
function("10",2,10,5,[1,1],"A")
function("10",15,44,4,[13,1],"B")
function("12,253,15",4,41,4,[2,1],"B")
function("12,253,15",1,7,17,[1,13],"A")
function("12,253,15",1,17,30,[1,26],"A")
function("12,253,15",1,7,52,[1,48],"A")
function("16,20,25,27,30,35",2,2,2,[1,1],"B")
function("16,20,25,27,30,35",8,48,2,[7,1],"B")
function("16,20,25,27,30,35",5,10,8,[1,6],"B")
function("16,20,25,27,30,35",1,6,9,[1,6],"A")
function("16,20,25,27,30,35",1,29,19,[1,17],"A")
function("16,20,25,27,30,35",2,12,52,[1,49],"A")
function("16,20,25,27,30,35",1,7,66,[1,64],"A")
function("16,20,25,27,30,35",8,19,65,[1,64],"B")
function("37,40,45",1,26,4,[1,1],"A")
function("37,40,45",13,13,3,[11,1],"B")
function("37,40,45",19,34,3,[18,1],"B")
function("50,55",2,31,6,[1,1],"A")
function("50,55",11,43,4,[9,1],"B")
function("60, 65,100(민자포함)",2,10,4,[1,1],"A")
function("60, 65,100(민자포함)",14,23,3,[12,1],"B")
function("60, 65,100(민자포함)",2,33,15,[1,14],"B")
function("60, 65,100(민자포함)",1,11,30,[1,26],"A")
function("102,104,110,120,151,153",2,4,4,[1,1],"A")
function("102,104,110,120,151,153",15,22,3,[13,1],"B")
function("102,104,110,120,151,153",1,4,16,[1,14],"A")
function("102,104,110,120,151,153",15,19,16,[13,14],"B")
function("102,104,110,120,151,153",2,7,29,[1,26],"A")
function("102,104,110,120,151,153",13,18,28,[13,26],"A")
function("251.300,451,551",1,8,3,[1,1],"A")
function("251.300,451,551",14,20,3,[14,1],"A")
function("251.300,451,551",1,5,18,[1,16],"A")
function("251.300,451,551",14,17,18,[14,16],"A")
function("17,25,55,110,130,171,400",1,6,3,[1,1],"A")
function("17,25,55,110,130,171,400",10,10,3,[10,1],"A")
function("17,25,55,110,130,171,400",17,19,3,[17,1],"A")
function("17,25,55,110,130,171,400",1,9,13,[1,11],"A")
function("17,25,55,110,130,171,400",13,20,13,[13,11],"A")
function("17,25,55,110,130,171,400",2,4,26,[1,23],"A")
function("17,25,55,110,130,171,400",9,9,27,[1,23],"A")
function("17,25,55,110,130,171,400",13,20,25,[13,23],"A")
function("17,25,55,110,130,171,400",1,6,35,[1,33],"A")

l2 = list(s)
l = sorted(l)
l2 = sorted(l2)
print(l)
print(l2)

for i in range(len(l)-1):
    if l[i] == l[i+1] and l[i].find('J')==-1:
        print(l[i])

"""
    #print(strList)
    
    edgeList=[]
    minEdgeList=[]
    if type == "A":
        for i in range(xy1[0],xy2[0]):
            edgeList.clear()
            for j in range(i+diff,xy2[1]+1):
                edgeList.append(ws.Cells(j,i).Value)
            minEdgeList.append([strList[i-xy1[0]],strList[j-xy1[1]],min(edgeList)])
    else:
        for i in range(xy1[1],xy2[1]):
            edgeList.clear()
            for j in range(i+diff,xy2[0]+1):
                edgeList.append(ws.Cells(i,j).Value)
            minEdgeList.append([strList[i-xy1[1]],strList[j-xy1[0]],min(edgeList)])

    
    for m in minEdgeList:
        print("graph.addWeightedEdge(str1:\"%s\", str2:\"%s\", weight: %.2f);"%(m[0],m[1],m[2]))
    """