from bs4 import BeautifulSoup

data = open("c:/users/crazy/pictures/movie.html",encoding="utf-8").read()
soup = BeautifulSoup(data,"html.parser")
lists = soup.find_all("li")
result = [(i.div.next_sibling.div.text,float(i.div.next_sibling.div.next_sibling.text[1:])) for i in lists]
result = sorted(result, key=lambda arg: arg[1], reverse=True)
print(*[f"{a} {b}" for a,b in result],sep="\n")