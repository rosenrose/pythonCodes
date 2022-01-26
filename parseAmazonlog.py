import subprocess
import json
import sys
from pathlib import Path

rclonePath = Path("D:/install/rclone")
logPath = "amazonlog:rosenrose-log/rosenrose"

result = subprocess.run(["rclone","ls",logPath],encoding="utf-8",cwd=rclonePath,capture_output=True).stdout.decode("utf-8")
result = result.split("\n")

logList = [i.split(" ")[-1] for i in result][:-1]

def deleteLog():
    for log in logList[0:int(sys.argv[2])]:
        #print(logPath+"/"+log)
        subprocess.run([rclonePath/"rclone","delete",logPath+"/"+log])

def printLog():
    size = 0
    for log in logList[int(sys.argv[2])*-1:]:
        subprocess.run([rclonePath/"rclone","copy",logPath+"/"+log,rclonePath])
        with (rclonePath/log).open(encoding="utf-8") as f:
            content = f.read().split("\n")[:-1]

        for line in content:
            pos1 = line.find(" ")
            pos2 = line.find(" ",pos1+1)
            bucket = line[pos1+1:pos2]

            pos1 = line.find("[",pos2+1)
            pos2 = line.find("]",pos1+1)
            time = line[pos1+1:pos2]

            pos1 = line.find(" ",pos2+1)
            pos2 = line.find(" ",pos1+1)
            ip = line[pos1+1:pos2]

            pos1 = line.find("OBJECT",pos2+1)
            pos2 = line.find("\"",pos1+7)
            file = line[pos1+7:pos2].strip()

            pos1 = line.find("\"",pos2+2)
            pos2 = line.find(" ",line.find(" ",pos1+2)+1)
            stat = line[pos1+2:pos2]

            pos1 = line.find("\"",pos2+1)
            pos2 = line.find("\"",pos1+1)
            refer = line[pos1+1:pos2]

            pos1 = line.find("\"",pos2+1)
            pos2 = line.find("\"",pos1+1)
            agent = line[pos1+1:pos2]

            if agent.find("rclone") == -1 and len(file) < 100:
                print("시간: "+time)
                print("IP: "+ip)
                print("버킷: "+bucket)
                print("파일: "+file)
                print("상태: "+stat)
                print("요청지: "+refer)
                print("브라우저: "+agent)
                print("="*10)

            #if agent.find("Google") != -1:
            bucket = "amazon%s:%s"%(bucket,bucket)
            sizeJson = subprocess.run(["rclone","size","--json",bucket+"/"+file],encoding="utf-8",cwd=rclonePath,capture_output=True).stdout.decode("utf-8")
            sizeJson = json.loads(sizeJson)
            size = size + sizeJson["bytes"]
        (rclonePath/log).unlink()
    print("%.2f MB, %.2f GB"%(size/(1024**2),size/(1024**3)))

if sys.argv[1] == "del":
    deleteLog()
elif sys.argv[1] == "print":
    printLog()
elif sys.argv[1] == "length":
    print(len(logList))