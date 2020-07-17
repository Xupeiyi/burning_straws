import os

from config import BASE_URL, DEST_DIR
import requests
from bs4 import BeautifulSoup


def get_pdf(pdf_link):
    resp = requests.get(pdf_link)
    return resp.content


def save_pdf(pdf, file_name):
    path = os.path.join(DEST_DIR, file_name + '.pdf')
    with open(path, 'wb') as fp:
        fp.write(pdf)


def is_pdf_tag(tag):
    try:
        return tag['href'].endswith('pdf')
    except KeyError:
        return False


def get_pdf_links_and_names(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    tags = soup.findAll('a')
    pdf_links_and_names = [(BASE_URL + tag['href'].lstrip('.'), tag.text)
                           for tag in tags if is_pdf_tag(tag)]
    return pdf_links_and_names


def download_single_page(page_url):
    pdf_links_and_names = get_pdf_links_and_names(page_url)
    for pdf_link, pdf_name in pdf_links_and_names:
        pdf = get_pdf(pdf_link)
        save_pdf(pdf, pdf_name)
    print(f"page {page_url} downloaded!")