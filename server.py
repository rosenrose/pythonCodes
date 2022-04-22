from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36"}
galleries = [("디제이맥스","djmaxrespect"),("사이터스","rayarkcytus"),("지브리","ghibli"),("하프라이프","halflife3"),("보이즈","voezvalkyrie"),("디모","deemo"),("동방","touhou")]
replaces = [(r"(노|놐|누|눜)([.,!?;ㄱ-ㅎ]*\s+)","냐\g<2>"),(r"(노|놐|누|눜|이기)([.,!?;ㄱ-ㅎ]*)$","냐\g<2>"),("되노","되냐"),("뭐노","뭐냐"),("무친","미친"),("무쳤","미쳤"),("노무","너무"),("운지","좆망"),("(했|햇)(노|누)","했냐"),(r"돼\s*(겠|고|나|냐|네|는|니|다|던|든|어)","되\g<1>"),(r"되\s*(가|도[^록]|버|봐|서|선|야|와|요|있|주|줘|\s)","돼\g<1>")]

def normalize(url):
    response = requests.get(url, headers=headers)
    content = response.content.decode("utf-8")
    content = content.replace("https://m.dcinside.com/board","")
    content = content.replace("https://www.dogdrip.net/","")
    soup = BeautifulSoup(content, "html.parser")
    for s in soup.select("script"): s.decompose()
    textNodes = [i for i in soup.find_all(string=True) if i.strip() and (i.parent.name not in ['style','script','head','title','meta','[document]'])]
    for text in textNodes:
        for regex in replaces:
            compiled = re.compile(regex[0])
            if result := compiled.search(text):
                # print(result[0]," || ",compiled.sub(regex[1],text))
                try:
                    text.replace_with(compiled.sub(regex[1],text))
                except Exception as e:
                    pass
    return soup

@app.route('/')
def index():
    return render_template("gallery.html", galleries=galleries)

@app.route('/<id>')
def gall(id):
    params = "&".join([f"{i[0]}={i[1]}" for i in request.args.items()])
    soup = normalize(f"https://m.dcinside.com/board/{id}?{params}")
    try:
        soup.select("ul.tab-lst")[1].select_one("li:nth-child(2) > a")["href"] = f"/{id}?recommend=1"
        regex = re.compile(r"\((.*)\)")
        for mal in soup.select("ul.mal-lst a"):
            mal["href"] = f"/{id}?headid={regex.search(mal['href'])[1]}"
        title = soup.select_one("a.gall-tit-lnkempty")
        title["href"] = f"https://m.dcinside.com/board/{id}?{params}"
        title["target"] = "_blank"
    except Exception as e:
        pass
    return str(soup)

@app.route('/<id>/<no>')
def doc(id, no):
    params = "&".join([f"{i[0]}={i[1]}" for i in request.args.items()])
    soup = normalize(f"https://m.dcinside.com/board/{id}/{no}?{params}")
    for img in soup.select("div.gall-thum-btm-inner img"):
        if img.has_attr("data-original"):
            img["src"] = img["data-original"]
    try:
        title = soup.select_one("div.gallview-tit-box > span.tit")
        title.name = "a"
        title["href"] = f"https://m.dcinside.com/board/{id}/{no}?{params}"
        title["target"] = "_blank"
    except Exception as e:
        pass
    # a = soup.new_tag("a", href=f"https://m.dcinside.com/board/{id}/{no}?{params}")
    # a.string = f"{id}/{no}"
    # title.append(a)
    return str(soup)

@app.route('/dogdrip')
def dog():
    params = "&".join([f"{i[0]}={i[1]}" for i in request.args.items()])
    soup = normalize(f"https://www.dogdrip.net/?{params}")
    print(soup)
    return str(soup)

@app.route('/dogdrip/<board_doc>')
def dog_board_doc(board_doc):
    params = "&".join([f"{i[0]}={i[1]}" for i in request.args.items()])
    soup = normalize(f"https://www.dogdrip.net/{board_doc}?{params}")
    if board_doc.isdigit():
        doc = board_doc
    else:
        board = board_doc
    return str(soup)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)