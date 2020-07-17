import os
import time
import sys

import requests
from bs4 import BeautifulSoup




def PAGE_URLS():
    for i in  range(1, 20):
        yield f"{BASE_URL}/index_{i}.shtml"


def is_pdf_tag(tag):
    try:
        href = tag['href']
        return tag['href'].endswith('pdf')
    except KeyError:
        return False
        

def pdf_url(pdf_tag):
    res = BASE_URL + pdf_tag['href'].lstrip('.')
    return res


def get_pdf(pdf_link):
    resp = requests.get(pdf_link)
    return resp.content 


def save_pdf(pdf,file_name):
    path = os.path.join(DEST_DIR, file_name)
    with open(path, 'wb') as fp:
        fp.write(pdf)


def get_pdf_links(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    tags = soup.findAll('a')
    pdf_links = [pdf_url(tag) for tag in tags if is_pdf_tag(tag)]
    return pdf_links


def download_single_page(url):
    pdf_links = get_pdf_links(url)
    for pdf_link in pdf_links:
        file_name = pdf_link.split('/')[-1]
        pdf = get_pdf(pdf_link)
        save_pdf(pdf, file_name)
    print(f"page {url} downloaded!")


def timer(f):
    def decorated(*args, **kwargs):
        t0 = time.time()
        count = f(*args, **kwargs)
        elapsed = time.time() - t0
        msg = "\n{} pages downloaded in {:.2f}s"
        print(msg.format(count, elapsed))
    return decorated


@timer
def download_many():
    count = 0
    for url in PAGE_URLS():
        download_single_page(url)
        count += 1
    print("All downloaded!")
    return count
    
    
if __name__ == '__main__':
    download_many()
    
    

