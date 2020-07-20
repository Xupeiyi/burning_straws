import asyncio

import aiohttp
from bs4 import BeautifulSoup

from scrapers.config import BASE_URL
from scrapers.scraper import is_pdf_tag, save_pdf


async def get_pdf_links_and_names(url):
    resp = await aiohttp.request('GET', url)
    html = await resp.read()
    
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.findAll('a')
    pdf_links_and_names = [(BASE_URL + tag['href'].lstrip('.'), tag.text)
                           for tag in tags if is_pdf_tag(tag)]
    return pdf_links_and_names


async def get_pdf(pdf_link):
    resp = await aiohttp.request('GET', pdf_link)
    pdf = await resp.read()
    return pdf


async def download_one(pdf_link, pdf_name):
    pdf = await get_pdf(pdf_link)
    save_pdf(pdf, pdf_name)
 
    