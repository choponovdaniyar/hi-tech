import json
import grequests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


HEADERS = {
    "user-agent": UserAgent().random
}


def get_links():
    url = "https://hi-tech.news"
    resp = grequests.map([grequests.get(url, headers = HEADERS)])[0]
    with open("data/index.html", "w", encoding = "utf-8") as f:
        f.write(resp.text)
    


    with open("data/index.html", "r", encoding = "utf-8") as f:
        resp = f.read()
    soup = BeautifulSoup(resp, "lxml")
    pagination = soup.find("span", class_ = "navigations").find_all("a")
    max_pages = int(pagination[-1].attrs["href"].split("/")[-2])
    pages = []
    for page in range(max_pages):
        pages += [grequests.get(f"https://hi-tech.news/page/{page + 1}")]
    pages = grequests.map(pages)
    for page in range(max_pages):
        with open(f"data/page{page + 1}.html", "w", encoding="utf-8") as f:
            f.write(pages[page].text)



    for page in range(122):
        with open(f"data/pages/page{page + 1}.html", "r", encoding="utf-8") as f:
            html = f.read()
            soup = BeautifulSoup(html, 'lxml')
        items = [x.attrs['href'] for x in soup.find("div", class_ = "blog-posts").find_all("a",  class_="post-title-a")]
        print( "\n".join(items))
        with open("links.txt", "a", encoding="utf-8") as f:
            f.write( "\n".join(items))

def get_post_info(link):
    resp = grequests.map([grequests.get(link, headers = HEADERS)])[0]
    soup = BeautifulSoup(resp.text, "lxml")

    title = soup.find("div", class_ = "post").find("div", class_ = "post-content").find("h1", class_ = "title").text
    date = soup.find("div", class_ = "post").find("div", class_ = "tile-views").text
    image = f'https://hi-tech.news{soup.find("div", class_ = "post").find("div", class_ = "post-media-full").find("img").attrs["src"]}'
    text = soup.find("div", class_ = "post").find("div", class_ = "post-content").find("div", class_ = "the-excerpt").text.replace("\n", "")   
    
    return {
        "link": link,
        "title": title,
        "date": date,
        "image": image,
        "text": text
    }

def scraping():
    with open("links.txt", "r", encoding="utf-8") as f:
        links = f.read()
        links = links.split("\n")

    res = list()
    for x in links:
        res += [get_post_info(x)]
        print(x)
    with open("info.json", "w", encoding="utf-8") as f:
        json.dump(res,f, indent=4, ensure_ascii=False)
if __name__ == "__main__":
    get_links() 
    scraping()