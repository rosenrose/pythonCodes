def replaceSpecialCh(title):
    replaceDic = {"\\":"＼", "/":"／", ":":"：", "*":"＊", "?":"？", "\"":"＂", "<":"〈", ">":"〉", "|":"｜",
                    "#":"＃", ".":"．"}
    for r in replaceDic:
        title = title.replace(r,replaceDic[r])
    return title