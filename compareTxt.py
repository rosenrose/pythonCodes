data1 = open("file1.txt",encoding="utf-8").read().splitlines()
data2 = open("file2.txt",encoding="utf-8").read().splitlines()

for i,line in enumerate(data1):
    if line != data2[i]:
        print(f"{line} → {data2[i]}")