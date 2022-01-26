data = open("c:/users/crazy/pictures/new 1.txt","rb").read()
result = bytearray()
a = set()
b = set()
i = 0
while i < len(data):
    if (byte:=data[i]) < 128:
        result.append(byte)
    elif byte == 194:
        i += 1
        result.append(data[i])
        a.add(data[i])
    elif byte == 195:
        i += 1
        result.append(data[i]+64)
        b.add(data[i])
        # b.append(data[i]+64)
    i += 1
print(min(a),max(a))
print(min(b),max(b))
c = sorted(set(open("E:/Enjoy!/IPX-192_720.srt",encoding="utf-8").read()))
print(c.index("가"), len(c))
input()
print(result.decode("utf-8"))
open("c:/users/crazy/pictures/new 2.txt","wb").write(result)