import os

from scrapers.config import BASE_URL, DEST_DIR
import requests
from bs4 import BeautifulSoup


def get_content(url):
    resp = requests.get(url)
    return resp.content


def gen_path(file_name):
    path = ''
    if '环境卫星' in file_name:
        path += '/环境卫星'
    elif '气象卫星' in file_name:
        path += '/气象卫星'

    if '日报' in file_name:
        path += '/日报'
    elif '月报' in file_name:
        path += '/月报'
        
    path = os.path.join(DEST_DIR + path, file_name + '.pdf')
    return path
    

def save_pdf(pdf, path):
    with open(path, 'wb') as fp:
        fp.write(pdf)


def is_target_file(file_name):
    return ('日报' in file_name or '月报' in file_name) and ('环境卫星' in file_name or '气象卫星' in file_name)


def is_target_pdf_tag(tag):
    try:
        return tag['href'].endswith('pdf') and is_target_file(tag.text)
    except KeyError:
        return False


def get_pdf_links_and_names(html):
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.findAll('a')
    pdf_links_and_names = [(BASE_URL + tag['href'].lstrip('.'), tag.text)
                           for tag in tags if is_target_pdf_tag(tag)]
    return pdf_links_and_names


def download_single_page(page_link):
    html = get_content(page_link)
    pdf_links_and_names = get_pdf_links_and_names(html)
    for pdf_link, pdf_name in pdf_links_and_names:
        pdf = get_content(pdf_link)
        path = gen_path(pdf_name)
        save_pdf(pdf, path)
    print(f"page {page_link} downloaded!")
    

