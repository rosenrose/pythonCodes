import random
import sys

def QuickSort(input_list):
    length = len(input_list)
    if length>1:
        pivot = input_list[int(length/2)]
        i = 0
        j = length-1
        while(i<=j):
            while(input_list[i]<pivot): i+=1
            while(input_list[j]>pivot): j-=1
            if i>j: break
            input_list[i],input_list[j] = input_list[j],input_list[i]
            i+=1; j-=1
        input_list[:j+1] = QuickSort(input_list[:j+1])
        input_list[i:] = QuickSort(input_list[i:])
    return input_list

# while(True):
#     input_list = [random.randrange(1000000) for i in range(random.randrange(1000000))]
#     comp = sorted(input_list)
#     input_list = QuickSort(input_list)
#     if comp == input_list:
#         print("equal")
#     else:
#         input("not equal")
N = int(input())
input_list = []
for i in range(N):
    input_list.append(int(sys.stdin.readline()))
print(QuickSort(input_list))