import json
import sys
import pyperclip
import re
data = json.load(open("d:/git/djmax.github.io/list.json",encoding="utf-8"))
# print(list(data["songs"].values())[0])

def run():
    levels = ["NM","HD","MX","SC"]
    for game in data["songs"]:
        for i,song in enumerate(data["songs"][game]):
            if not "level" in song:
                print(song["title"])
                song["level"] = {"4B":{},"5B":{},"6B":{},"8B":{}}
                for btn in song["level"]:
                    for j in levels:
                        level = input(f"{btn} {j}: ").strip()
                        if level == "q" or level == "Q":
                            return    
                        elif (level):
                            song["level"][btn][j] = int(level)
                print(json.dumps(song,ensure_ascii=False,indent=2),"\n")
                data["songs"][game][i] = song
                json.dump(data,open("d:/git/djmax.github.io/list.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)

def check():
    rank = ["NM","HD","MX","SC"]
    start = int(sys.argv[3])
    for num,song in enumerate(data["songs"][sys.argv[2]][start-1:]):
        input(str(num+start)+" "+song["title"])
        # csv = open("d:/git/djmax.github.io/temp.csv").read().splitlines()
        csv = re.compile(r"\s*\[\d+\]").sub("",pyperclip.paste()).splitlines()
        assert len(csv) % 4 == 0
        
        rows = len(csv) // 4
        for i in range(len(csv)):
            if i % rows == 0:
                button = csv[i]
            else:
                message = button+","+rank[i%rows-1]
                if csv[i].isdecimal():
                    assert int(csv[i]) == song["level"][button][rank[i%rows-1]], message
                else:
                    assert not rank[i%rows-1] in song["level"][button], message

if __name__ == "__main__":
    if sys.argv[1] == "run": run()
    elif sys.argv[1] == "check": check()