import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup

from scrapers.config import BASE_URL, PAGE_URLS
from scrapers.scraper import is_target_pdf_tag, gen_path, get_pdf_links_and_names
from scrapers.utils import timer


async def get_content_asnyc(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.content.read()
    return content

# async def get_pdf_links_and_names(url):
#
#     soup = BeautifulSoup(html, 'lxml')
#     tags = soup.findAll('a')
#     pdf_links_and_names = [(BASE_URL + tag['href'].lstrip('.'), tag.text)
#                            for tag in tags if is_target_pdf_tag(tag)]
#     return pdf_links_and_names


async def save_pdf_async(pdf, path):
    async with aiofiles.open(path, 'wb') as fp:
        await fp.write(pdf)


async def download_one(args):
    pdf_link, pdf_name = args
    path = gen_path(pdf_name)
    pdf = await get_content_asnyc(pdf_link)
    await save_pdf_async(pdf, path)


@timer
def download_one_page(page_link):
    pdf_links_and_names = get_pdf_links_and_names(page_link)
    loop = asyncio.get_event_loop()
    to_do = [download_one(args) for args in pdf_links_and_names]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)

# def download_many()


if __name__ == '__main__':
    page_link = PAGE_URLS().__next__()
    download_one_page(page_link)
