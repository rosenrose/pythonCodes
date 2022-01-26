import os
import sys

def writeLog(msg):
    with open("c:/users/crazy/pictures/python/editTag.log","a",encoding="utf-8") as a:
        a.write(msg)

def convertTag(options):
    if options[0] == "del":
        os.remove(os.path.join(folder1,f"{options[1]}.md"))
        print(f"{options[1]} delete")
        writeLog(f"{options[1]} delete\n")
    elif options[0] == "rename":
        with open(os.path.join(folder1,f"{options[1]}.md"),"w",encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"name: \"{options[2]}\"\n")
            f.write(f"title: \"{options[2]}\"\n")
            f.write("---")

        if os.path.exists(os.path.join(folder1,f"{options[2]}.md")):
            os.remove(os.path.join(folder1,f"{options[1]}.md"))
            print(f"{options[2]}.md already exists, delete {options[1]}.md")
            writeLog(f"{options[2]}.md already exists, delete {options[1]}.md\n")
        else:
            os.rename(os.path.join(folder1,f"{options[1]}.md"),os.path.join(folder1,f"{options[2]}.md"))
            print(f"{options[1]}.md rename to {options[2]}.md")
            writeLog(f"{options[1]}.md rename to {options[2]}.md\n")
    
def convertPost(options):
    for post in os.listdir(folder2):
        lines = open(os.path.join(folder2,post),encoding="utf-8").readlines()

        tagList = lines[2][7:-2].split(" ")
        if options[1] not in tagList:
            continue

        if options[0] == "find":
            print(post)
        elif options[0] == "del":
            tagList.remove(options[1])
            print(f"{post}: delete {options[1]}")
            writeLog(f"{post}: delete {options[1]}\n")
        elif options[0] == "rename":
            if options[2] in tagList:
                tagList.remove(options[1])
                print(f"{post}: {options[2]} already exists, delete {options[1]}")
                writeLog(f"{post}: {options[2]} already exists, delete {options[1]}\n")
            else:
                for i in range(len(tagList)):
                    if tagList[i] == options[1]:
                        tagList[i] = options[2]
                        print(f"{post}: change {options[1]} to {options[2]}")
                        writeLog(f"{post}: change {options[1]} to {options[2]}\n")
                        break
        tags = ""
        for i in range(len(tagList)):
            tags = tags + tagList[i]
            if i < len(tagList)-1:
                tags = tags + " "
        lines[2] = f"tags: \"{tags}\"\n"

        with open(os.path.join(folder2,post),"w",encoding="utf-8") as f:
            for line in lines:
                f.write(line)

folder1 = "c:/users/crazy/pictures/rosenrose.github.io/_tags"
folder2 = "c:/users/crazy/pictures/rosenrose.github.io/_posts"
convertTag(sys.argv[1:])
convertPost(sys.argv[1:])