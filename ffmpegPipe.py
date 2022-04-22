import sys
import subprocess
import requests

def down(url):
    print(url)
    return requests.get(url).content

def inputImages():
    url = "https://d2wwh0934dzo2k.cloudfront.net/ghibli/05 마녀 배달부 키키 (1989)"
    images = [down(f"{url}/{500 + i:05}.jpg") for i in range(12)]

    proc = subprocess.Popen(["ffmpeg", "-f", "jpeg_pipe", "-framerate", "12", "-i", "pipe:", "-loop", "0", "a.webp", "-y"], stdin=subprocess.PIPE)

    try:
        # proc.communicate(input=images, timeout=10) 안됨
        for image in images:
            proc.stdin.write(image)
        proc.stdin.close()
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.terminate()
    proc.terminate()

def outputImage():
    # proc = subprocess.run(["ffmpeg", "-ss", "10", "-i", "c:/users/crazy/pictures/lou1.mkv", "-frames", "1", "-f", "image2", "-c:v", "png", "pipe:1"], capture_output=True)
    # output = proc.stdout
    # open("c:/users/crazy/pictures/a.png", "wb").write(output)

    proc = subprocess.Popen(["ffmpeg", "-ss", "10", "-i", "c:/users/crazy/pictures/lou1.mkv", "-frames", "1", "-f", "image2", "-c:v", "png", "pipe:1"], stdout=subprocess.PIPE, stderr=sys.stderr)

    with open("c:/users/crazy/pictures/a.png", "wb") as fp:
        while bytes := proc.stdout.read():
            fp.write(bytes)

    # while bytes := proc.stderr.read():
    #     print(bytes.decode("utf-8"))
    proc.terminate()

def outputImages():
    format = "jpg"
    proc = subprocess.run(["ffmpeg", "-ss", "100", "-to", "101", "-i", "c:/users/crazy/pictures/lou1.mkv", "-f", "image2pipe", "-q:v", "0", "-c:v", "mjpeg", "pipe:1"], capture_output=True)
    output = proc.stdout
    head = {
        "png": b"\x89\x50\x4E\x47",
        "jpg": b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46"
    }
    imgs = [head[format] + i for i in output.split(head[format])[1:]]
    print(len(output)/(1024**2), len(imgs))
    for i, img in enumerate(imgs):
        # open(f"c:/users/crazy/pictures/{i + 1:02}.{format}", "wb").write(img)
        p = subprocess.Popen(["rclone", "rcat", f"amazon_rosenrose:/rosenrose/test/{i + 1:02}.{format}", "-v", "-P"], stdin=subprocess.PIPE)
        p.stdin.write(img)
        p.stdin.close()
        p.terminate()

    # proc = subprocess.Popen(["ffmpeg", "-ss", "100", "-to", "101", "-i", "c:/users/crazy/pictures/lou1.mkv", "-f", "image2pipe", "-c:v", "png", "pipe:1"], stdout=subprocess.PIPE)
    # while bytes := proc.stdout.read():
    #     print(len(bytes))

if __name__ == "__main__":
    # inputImages()
    # outputImage()
    outputImages()