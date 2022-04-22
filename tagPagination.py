import copy
import re
from pathlib import Path
from bs4 import BeautifulSoup

path = Path("D:/Touhou/rosenrose.github.io/_site/tags")
paginate = 30

for dir in [i for i in path.iterdir() if i.is_dir()]:
    content = (dir/"index.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(content,"html.parser")
    postList = soup.find("ul",id="post-list").find_all("li")

    if len(postList) > paginate:
        template = copy.copy(soup)
        postLink = []
        postImg = []

        for i in template.find_all("li",class_="post-item post"):
            postLink.append(i.extract())
        for i in template.find_all("div",class_="post-image"):
            postImg.append(i.extract())
        
        pages = int(((len(postList)-1)/paginate))+1

        a = soup.new_tag("a",attrs={"href":"","id":"randomLink"})
        a.append(soup.new_tag("input",attrs={"type":"button","value":"랜덤 이동"}))
        template.find("div",class_="container",id="cover").append(a)

        script = soup.new_tag("script",type="text/javascript")
        allTags = [i.find("a")["href"] for i in postLink]
        script.string = f"""
            var allTags = {str(allTags)};
            var random = Math.floor(Math.random() * allTags.length);
            document.getElementById(\"randomLink\").href = allTags[random]
        """
        template.find("div",class_="container",id="cover").append(script)
        #print(f"{dir} {len(postList)}: {pages}")
        for pageNum in range(1,pages+1):
            temp = copy.copy(template)

            pager = soup.new_tag("ul",attrs={"class":"pager main-pager"})
            temp.find("div",class_="container",role="main").find("div",class_=re.compile("col*")).append(pager)

            pageMover = soup.new_tag("div",attrs={"class":"pageMover"})
            pageMover.append(soup.new_tag("input",type="text",id="pageNumInput",style="width:48px"))
            pageMover.append(soup.new_tag("input",type="button",value="이동",onclick="movePage();"))
            script = soup.new_tag("script",type="text/javascript")
            script.string = f"""
                function movePage() {{
                var pageNum = document.getElementById("pageNumInput").value;
                location.href = "/touhou/tags/{dir.name}/page"+pageNum
            }}"""
            pageMover.append(script)
            temp.find("div",class_="container",role="main").find("div",class_=re.compile("col*")).append(pageMover)

            for i in range((pageNum-1)*paginate,min(pageNum*paginate,len(postList))):
                temp.find("ul",id="post-list").append(postLink[i])
                temp.find("ul",id="post-list").append(postImg[i])

            if pageNum > 3:
                home = soup.new_tag("li",attrs={"class":"home"})
                a = soup.new_tag("a",href=f"/touhou/tags/{dir.name}/")
                a.string = "← 처음"
                home.append(a)
                pager.append(home)
            for i in range(max(pageNum-2,1),pageNum):
                li = soup.new_tag("li")
                if i==1:
                    a = soup.new_tag("a",href=f"/touhou/tags/{dir.name}/")
                else:    
                    a = soup.new_tag("a",href=f"/touhou/tags/{dir.name}/page{i}")
                a.string = str(i)
                li.append(a)
                pager.append(li)
            li = soup.new_tag("li")
            li.string = str(pageNum)
            pager.append(li)
            for i in range(pageNum+1,min(pageNum+3,pages+1)):
                li = soup.new_tag("li")
                a = soup.new_tag("a",href=f"/touhou/tags/{dir.name}/page{i}")
                a.string = str(i)
                li.append(a)
                pager.append(li)
            if pageNum < pages-2:
                end = soup.new_tag("li",attrs={"class":"end"})
                a = soup.new_tag("a",href=f"/touhou/tags/{dir.name}/page{pages}/")
                a.string = f"끝({pages}) →"
                end.append(a)
                pager.append(end)

            if pageNum > 1:
                temp.find("meta",property="og:url")["content"] = temp.find("meta",property="og:url")["content"]+f"page{pageNum}/"
                temp.find("link",rel="canonical")["href"] = temp.find("link",rel="canonical")["href"]+f"page{pageNum}/"
                (dir/f"page{pageNum}").mkdir(parents=True)
                f = open(dir/f"page{pageNum}"/"index.html","w",encoding="utf-8")
            else:
                f = open(dir/"index.html","w",encoding="utf-8")
            f.write(str(temp))
            f.close()
