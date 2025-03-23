from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
import sys

text_splitter = RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=100,length_function=len)

def get_base(url):
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    return base

def crawl(start,limit):
    base_domain = get_base(start)

    links = [start]
    visited = []
    txt = ""

    while links and len(visited) < limit:
        to_visit = links.pop(0)
        visited.append(to_visit)

        html = req.get(to_visit).text
        soup = BeautifulSoup(html,"lxml")
        for anchor in soup.find_all("a",href=True):
            sublink = urljoin(to_visit,anchor["href"])
            sub_base = get_base(sublink)
            if not sublink in visited and base_domain == sub_base:
                links.append(sublink)
        visited.append(to_visit)
        txt += soup.get_text(" ",True) + "\n\n"
        sys.stdout.write("\r"+f"Crawling the site %{round((len(visited)/limit)*100)} done.")
        sys.stdout.flush()

    txt = text_splitter.split_text(txt)
    return txt