import urllib.request
import requests
import time

for i in range(37530,38000):
    Buf = urllib.request.urlopen("http://tvn-cloudfront.tving.com/tvn/s5/media-ux7biv1t3_%d.ts" %i)
    with open("c:/users/crazy/pictures/python/%d.ts" %i, "wb") as f:
        f.write(Buf.read())
    time.sleep(2)

