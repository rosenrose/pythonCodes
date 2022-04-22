import sys
import re
import requests
import time
import datetime
import subprocess
from bs4 import BeautifulSoup
from tkinter import messagebox
from pathlib import Path
from lxml import etree

domain = "https://wp.touhougarakuta.com"
nasPath = Path("Z:")


def search(url):
    print(f"Current url: {url}")
    response = requests.get(url + "?MD")
    soup = BeautifulSoup(response.text, "html.parser")

    pathName = url[len(domain) :]
    if not (localDir := nasPath / pathName).exist():
        localDir.mkdir(parents=True)

    rootList = soup.find("pre")
    icons = rootList.find_all("img")[2:]
    if len(icons) <= 1:
        print(f"{pathName} is empty")
        return
    links = rootList.find_all("a")[5:]

    dirList = []
    fileList = []
    for n, icon in enumerate(icons):
        if icon["alt"] == "directory":
            dirList.append(links[n]["href"])
        else:
            fileList.append(links[n].text)

    for child in dirList:
        search(domain + child)

    if set(fileList) <= set(localList := [str(i.name) for i in localDir.iterdir()]):
        print(f"Pass {pathName}")
    else:
        # messagebox.showinfo("new!")
        downList = [
            i for i in fileList if i not in localList and not i.endswith(".php")
        ]
        for file in downList:
            print("Download " + file)
            with (localDir / file).open("wb") as f:
                while True:
                    try:
                        data = requests.get(domain + pathName + file).content
                    except Exception as ex:
                        print(ex)
                        print(type(ex))
                        time.sleep(10)
                    else:
                        break
                f.write(data)


def check(url):
    try:
        response = requests.get(url)
    except Exception as ex:
        print(ex, url)
        time.sleep(600)
    else:
        if response.url != url or response.status_code == 404:
            pass
        else:
            messagebox.showinfo("uploaded", url)
    time.sleep(1)


def removeElement(*element):
    for elem in element:
        if elem is not None:
            elem.getparent().remove(elem)


def archive(path):
    index = path / "index.html"
    data = index.read_text(encoding="utf-8")
    chapter, comic = [i.stem for i in index.parents][:2]

    data = re.compile(r"\./[^>]+_files/").sub(f"", data)
    data = re.compile(r"<style data-href=.+?>").sub("<style>", data)
    data = re.compile(
        r"https://s3-ap-northeast-1.amazonaws.com/touhougarakuta-statics/putfykzd/wp-content/uploads/\d+/\d+/\d+/"
    ).sub("", data)
    # data = re.compile(r"logo-1.0.0.png\" style=\"height:\s*\d+px").sub("/saoow/logo-1.0.0.png\" style=\"height:25px", data)
    data = re.compile(r"href=\"https://touhougarakuta.com/index_.+?/.+?\"").sub(
        'href=".."', data
    )
    data = re.compile(
        r"href=\"https://touhougarakuta.com/novel/youseijintyouge_\d+\""
    ).sub('href=".."', data)
    data = re.compile(
        r"href=\"https://touhougarakuta.com/novel/youseijintyouge_\d+/1\""
    ).sub('href="1"', data)
    data = re.compile(r"src=\"jinchoge_sashie(\d+)-\d+x\d+.(jpg|png)\"").sub(
        'src="/saoow/youseijinchouge/illust_gallery/jinchoge_sashie\g<1>.\g<2>"', data
    )
    data = re.compile(r"srcset=\".+?\"").sub("", data)
    data = re.compile(r"※配信期限.+?\d+:\d+").sub("", data)
    data = data.replace("https://touhougarakuta.com/static/", "/saoow/static/")
    data = re.compile(r"\"https://touhougarakuta.com/?\"").sub('"/saoow/"', data)
    data = re.compile(
        r"\"(banner-2|(footer_)?logo-1\.0\.0|(([^\"]+?_)?icon|button)[^\"]+?)(\.(png|jpg|svg))\""
    ).sub('"/saoow/static/\g<1>\g<5>"', data)
    data = data.replace('"1.png"', '"/saoow/banner-1.png"')
    data = data.replace(
        '"1570093300351.jpg"', '"/saoow/youseijinchouge/1570093300351.jpg"'
    )
    data = data.replace(
        '"e9c1544d692a16930cb2fbcdf6935b61.jpg"',
        '"/saoow/youseijinchouge/e9c1544d692a16930cb2fbcdf6935b61.jpg"',
    )
    data = data.replace(
        "yosei_logo_fix.jpg", "/saoow/youseijinchouge/yosei_logo_fix.jpg"
    )
    data = data.replace("yosei_visual2.jpg", "/saoow/youseijinchouge/yosei_visual2.jpg")
    data = data.replace("【公開終了】", "")

    divRegex = re.compile(
        r"<div style=\"flex-direction: ?column;?\">(.+?)</div>", re.DOTALL
    )
    imgRegex = re.compile(r"(<img src=\")(.+?\">)", re.DOTALL)
    coverRegex = re.compile(
        r"(style=['\"]background-image: ?url\(\"?)(.+?\"?\);?['\"]>)", re.DOTALL
    )
    div = divRegex.search(data)
    if div:
        img = div[1]
        newImg = imgRegex.sub(
            f"\g<1>https://d2l1b145ht03q6.cloudfront.net/saoow/{comic}/{chapter}/\g<2>",
            img,
        )
        data = data.replace(img, newImg)
        cover = coverRegex.search(data)[0]
        newCover = coverRegex.sub(
            f"\g<1>https://d2l1b145ht03q6.cloudfront.net/saoow/{comic}/{chapter}/\g<2>",
            cover,
        )
        data = data.replace(cover, newCover)

    xml = etree.fromstring(data, parser=etree.HTMLParser(encoding="utf-8"))
    regexpNS = "http://exslt.org/regular-expressions"
    removeElement(*xml.findall(".//script"))
    removeElement(*xml.findall(".//iframe"))
    removeElement(xml.find(".//style[@class = 'vjs-styles-defaults']"))
    removeElement(
        *xml.xpath(
            "//link[re:test(@rel, 'prefetch|preload|sitemap|stylesheet')]",
            namespaces={"re": regexpNS},
        )
    )
    removeElement(
        *xml.xpath(
            "//meta[re:test(@name, 'google-site-verification|twitter:card|twitter:site|fb:app_id')]",
            namespaces={"re": regexpNS},
        )
    )
    removeElement(
        *xml.xpath(
            "//meta[re:test(@property, 'fb:app_id')]", namespaces={"re": regexpNS}
        )
    )
    removeElement(
        *xml.xpath(
            "//div[re:test(@class, 'background|nextArticle|discription|search|search_area|sns|banner|goog-|ReactModalPortal')]",
            namespaces={"re": regexpNS},
        )
    )
    removeElement(
        *xml.xpath("//div[re:test(@id, 'goog-')]", namespaces={"re": regexpNS})
    )
    removeElement(*xml.xpath("//h3[contains(text(), 'おすすめ記事')]"))
    removeElement(
        *xml.xpath(
            "//h3[re:test(text(), '同じカテゴリの記事|新着記事')]/..", namespaces={"re": regexpNS}
        )
    )
    etree.indent(xml, space="  ")
    xml = etree.tostring(
        xml, encoding="utf-8", method="html", doctype="<!DOCTYPE html>"
    )

    index.with_stem("original").write_text(
        index.read_text(encoding="utf-8"), encoding="utf-8"
    )
    index.write_text(xml.decode("utf-8"), encoding="utf-8")
    subprocess.run(
        [
            "rclone",
            "move",
            path.resolve(),
            f"amazon_rosenrose:/rosenrose/saoow/{comic}/{chapter}",
            "--include",
            "*.jpg",
            "-v",
            "-P",
        ],
        check=True,
    )


def ko(path):
    index = path / "index.html"
    data = index.read_text(encoding="utf-8")
    chapter, comic = [i.stem for i in index.parents][:2]

    data = data.replace('<html lang="ja"', '<html lang="ko"')
    data = data.replace(
        '<img src="/saoow/static/logo-1.0.0.png"',
        '<img src="/saoow/static/logo-1.0.0_ko.png"',
    )
    data = data.replace("　", " ")
    data = data.replace("第", "제")
    data = data.replace("話", "화")
    data = data.replace("前編", "전편")
    data = data.replace("中編", "중편")
    data = data.replace("後編", "후편")
    data = data.replace("東方我楽多叢誌", "동방가라쿠타총지")
    data = data.replace("東方外來韋編", "동방외래위편")
    data = data.replace("月刊コンプエース", "월간 콤프에이스")
    data = data.replace("原作", "원작")
    data = data.replace("東方Project", "동방Project")
    data = data.replace("漫画", "만화")
    data = data.replace("もくじ", "목차")
    data = data.replace("で読む", "에서 읽기")
    data = data.replace("出典元", "출전")
    data = data.replace("公式HPはコチラ", "공식 홈페이지")
    data = data.replace("公式Twitterはコチラ", "공식 트위터")
    data = data.replace("あらすじ", "줄거리")
    data = data.replace("目次へ", "목차로")
    data = data.replace("タグ", "태그")
    data = data.replace("동방Project関連サイト", "동방Project 연관 사이트")
    data = data.replace("上海アリス幻樂団 ホームページ", "상하이앨리스환악단 홈페이지")
    data = data.replace("ZUNさんのブログ「博麗幻想書譜」", "ZUN 씨의 블로그「하쿠레이환상서보」")
    data = data.replace("ZUNさんのツイッター", "ZUN 씨의 트위터")
    data = data.replace("東方よもやまニュース", "동방 요모야마 뉴스")
    data = data.replace("インタビュー", "인터뷰")
    data = data.replace("リポート", "리포트")
    data = data.replace("コラム", "칼럼")
    data = data.replace("同人誌評", "동인지 평")
    data = data.replace("音楽評", "음악 평")
    data = data.replace("ゲーム評", "게임 평")
    data = data.replace("동방가라쿠타총지とは", "동방가라쿠타총지란")
    data = data.replace("東方の遊び方", "동방을 즐기는 법")
    data = data.replace("イラスト", "일러스트")
    data = data.replace(
        """メールフォームは<a href="https://docs.google.com/forms/d/e/1FAIpQLSdtZpHXbsIM8KNlDW33aFr1ZI-b6selP2ElUhPcDratLeP7_g/viewform" target="_brank" rel="nofollow">
                        <span class="link_line">こちら</span>
                      </a>
                    </p>
                    <p class="original">「記事にしてほしい！」という連絡は<a href="https://touhougarakuta.com/news/press" target="_brank" rel="nofollow">
                        <span class="link_line">こちら</span>
                      </a>
                    </p>""",
        "Mail: touhou.garakuta@gmail.com</p>",
    )
    data = data.replace(f"/{comic}/{chapter}/", f"/{comic}_ko/{chapter}/")
    (kor := (base / f"{comic}_ko/{chapter}")).mkdir(exist_ok=True)
    (kor / "index.html").write_text(data, encoding="utf-8")
    input("pngTojpg")
    for png in kor.glob("*.png"):
        subprocess.run(
            ["ffmpeg", "-i", png, "-q:v", "0", png.with_suffix(".jpg"), "-y"],
            check=True,
        )
        png.unlink()
    subprocess.run(
        [
            "rclone",
            "-v",
            "-P",
            "move",
            "--include",
            "*.jpg",
            kor,
            f"amazon_rosenrose:/rosenrose/saoow/{comic}_ko/{chapter}",
        ],
        check=True,
    )


if __name__ == "__main__":
    base = Path("D:/git/saoow")
    if sys.argv[1] == "ko":
        for path in sys.argv[2:]:
            ko(base / path)
    else:
        for path in sys.argv[1:]:
            archive(base / path)
        # print(path)
        # for index in (base/path).rglob("index.html"):
        #     archive(index)
        # xml = etree.fromstring(index.read_text(encoding="utf-8"),parser=etree.HTMLParser(encoding="utf-8"))
        # removeElement(xml.find(".//meta[@name = 'google-site-verification']"))
        # removeElement(xml.find(".//meta[@name = 'twitter:card']"))
        # removeElement(xml.find(".//meta[@name = 'twitter:site']"))
        # removeElement(xml.find(".//meta[@property = 'fb:app_id']"))
        # xml = etree.tostring(xml,encoding="utf-8",method="html",doctype="<!DOCTYPE html>")
        # index.write_text(xml.decode("utf-8"),encoding="utf-8")

# while True:
#     search(domain+sys.argv[1])
#     search(domain+"/wp-content/uploads/2020/03/")

#     check(sys.argv[1])
#     print(datetime.datetime.today())
#     time.sleep(600)
