import asyncio
import aiohttp
from bs4 import BeautifulSoup

from scrapers.config import BASE_URL, PAGE_URLS
from scrapers.scraper import is_pdf_tag, save_pdf, get_pdf_links_and_names
from scrapers.utils import timer


# async def get_pdf_links_and_names(url):
#     resp = await aiohttp.ClientSession().get(url)
#
#     soup = BeautifulSoup(html, 'lxml')
#     tags = soup.findAll('a')
#     pdf_links_and_names = [(BASE_URL + tag['href'].lstrip('.'), tag.text)
#                            for tag in tags if is_pdf_tag(tag)]
#     return pdf_links_and_names


async def download_one(args):
    pdf_link, pdf_name = args
    
    async with aiohttp.ClientSession() as session:
        async with session.get(pdf_link) as resp:
            pdf = await resp.content.read()
            
    save_pdf(pdf, pdf_name)

 
@timer
def download_one_page(url):
    pdf_links_and_names = get_pdf_links_and_names(url)
    loop = asyncio.get_event_loop()
    to_do = [download_one(args) for args in pdf_links_and_names]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)


if __name__ == '__main__':
    url = PAGE_URLS().__next__()
    download_one_page(url)
