import struct

offsets = [(924,1),(1084,2),(1296,3),(1560,4),(1984,2),(2196,4),(2512,6),(2932,8),
            (3564,2),(3776,2),(3988,4),(4304,4),(4728,2),(4940,4),(5256,6),(5676,8),(6308,1),(6468,2),(6680,3),(6944,4)]
"""
with open("D:/Touhou/TouhouSuperExtractor1.2.5/th11/pl01b.sht","rb") as f:
    f.seek(0x28,0)
    data = f.read(0x240)
    i=0
    while(i<len(data)):
        print(struct.unpack('f',data[i:i+4])[0],struct.unpack('f',data[i+4:i+8])[0])
        i+=8
    
    data =(f.read())
    #data = bytearray(f.read())
with open("D:/Touhou/thcrap_brliron/rosenrose/test/th11/pl01b.sht","wb") as f:
    for i in offsets:
        for count in range(i[1]):
            data[i[0]+52*(2+count)+24:i[0]+52*(2+count)+28] = struct.pack('f',8)
            data[i[0]+52*(2+count)+29:i[0]+52*(2+count)+30] = int(1).to_bytes(1,"little")
            data[i[0]+52*(2+count)+36:i[0]+52*(2+count)+38] = int(1).to_bytes(2,"little")
            data[i[0]+52*(2+count)+40:i[0]+52*(2+count)+42] = int(1).to_bytes(2,"little")
    f.write(data)
    for i in offsets:
        for count in range(i[1]):
            f.seek(i[0]+52*(2+count)+24,0)
            f.write(struct.pack('f',8))
            f.seek(i[0]+52*(2+count)+36,0)
            f.write(int(1).to_bytes(2,"little"))
            f.seek(i[0]+52*(2+count)+40,0)
            f.write(int(1).to_bytes(2,"little"))"""