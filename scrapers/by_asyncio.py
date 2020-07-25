import asyncio
from itertools import chain

import aiohttp
import aiofiles

from scrapers.config import PAGE_URLS
from scrapers.scraper import gen_path, get_pdf_links_and_names
from scrapers.utils import timer, spin


async def get_content_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.content.read()
    return content


async def save_pdf_async(pdf, path):
    async with aiofiles.open(path, 'wb') as fp:
        await fp.write(pdf)


async def download_one_pdf(args):
    pdf_link, pdf_name = args
    spinner = asyncio.ensure_future(spin(f'downloading: {pdf_name}'))
    
    path = gen_path(pdf_name)
    pdf = await get_content_async(pdf_link)
    await save_pdf_async(pdf, path)
    
    spinner.cancel()


@timer
def download_many():
    loop = asyncio.get_event_loop()
    # get pdf_links from page_urls
    htmls_to_do = [get_content_async(page_url) for page_url in list(PAGE_URLS())[0:5]]
    htmls_wait_coro = asyncio.wait(htmls_to_do)
    htmls_res, _ = loop.run_until_complete(htmls_wait_coro)
    htmls = [r.result() for r in htmls_res]
    all_pdf_links_and_names = chain(*map(get_pdf_links_and_names, htmls))
    
    # get pdfs from pdf_links
    pdf_to_do = [download_one_pdf(args) for args in all_pdf_links_and_names]
    pdf_wait_coro = asyncio.wait(pdf_to_do)
    pdf_res, _ = loop.run_until_complete(pdf_wait_coro)
    count = len(pdf_res)
    
    loop.close()
    return count


if __name__ == '__main__':
    download_many()
