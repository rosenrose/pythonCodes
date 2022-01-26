from pathlib import Path
import sys

KILO = 1024
KB = KILO
MB = KILO**2
GB = KILO**3

option = ""

def folderSize(folder,result=0):
    if not folder.exists():
        print("Don't exist")
        return 0
        
    if option == "only code":
        for dir in [i for i in folder.iterdir() if i.is_dir()]:
            for file in dir.iterdir():
                result = result + file.stat().st_size
    else:
        for file in [i for i in folder.rglob("*") if i.is_file()]:
            result = result + file.stat().st_size
    return result

if __name__ == "__main__":
    if "-prefix" in sys.argv:
        folderList = [(Path(sys.argv[2])/i).resolve() for i in sys.argv[3:]]
    else:
        folderList = [Path(i).resolve() for i in sys.argv[1:]]
    result = 0
    for folder in folderList:
        result += folderSize(folder,result)    
    print(f"{result} Bytes\n{result/KB:.2f} KB\n{result/MB:.2f} MB\n{result/GB:.2f} GB")