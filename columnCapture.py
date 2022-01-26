import pyautogui
from PIL import Image
import diffimg

pyautogui.hotkey('alt','tab')

img1 = pyautogui.screenshot(region=(563,290,794,750))
imgList = []
imgList.append(img1.copy())
while True:
    pyautogui.press('down')
    img2 = pyautogui.screenshot(region=(563,290,794,750))
    #print(diffimg.diff(img1, img2))
    if diffimg.diff(img1, img2) < 0.01:
        break 
    img1 = img2.copy()
    imgList.append(img2.copy())

scroll = 1
while True:
    img1crop = imgList[-2].crop((0,scroll,imgList[-2].width,imgList[-2].height))
    img2crop = imgList[-1].crop((0,0,imgList[-1].width,imgList[-1].height-scroll))
    # print(diffimg.diff(img1crop, img2crop))
    if diffimg.diff(img1crop, img2crop) < 0.01:
        break
    scroll+=1
print(scroll)

bottom = imgList[1].crop((0,imgList[1].height-40,imgList[1].width,imgList[1].height))
newimg = Image.new("RGB",(imgList[0].width,imgList[0].height+bottom.height))
newimg.paste(imgList[0])
newimg.paste(bottom,(0,imgList[0].height))
for i in range(2,len(imgList)-1):
    bottom = imgList[i].crop((0,imgList[i].height-40,imgList[i].width,imgList[i].height))
    temp = newimg.copy()
    newimg = Image.new("RGB",(newimg.width,newimg.height+bottom.height))
    newimg.paste(temp)
    newimg.paste(bottom,(0,temp.height))
bottom = imgList[-1].crop((0,imgList[-1].height-scroll,imgList[-1].width,imgList[-1].height))
temp = newimg.copy()
newimg = Image.new("RGB",(newimg.width,newimg.height+bottom.height))
newimg.paste(temp)
newimg.paste(bottom,(0,temp.height))
newimg.save("c:/users/crazy/pictures/screenshots/capture.png")