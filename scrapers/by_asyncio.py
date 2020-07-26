import asyncio
from itertools import chain

import aiohttp
import aiofiles
import tqdm

from scrapers.config import PAGE_URLS
from scrapers.scraper import gen_path, get_pdf_links_and_names
from scrapers.utils import timer


MAX_CONCUR_REQ = 20


async def get_content_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.content.read()
    return content


async def save_pdf_async(pdf, path):
    async with aiofiles.open(path, 'wb') as fp:
        await fp.write(pdf)


async def download_one_pdf(semaphore, args):
    pdf_link, pdf_name = args
    path = gen_path(pdf_name)
    async with semaphore:
        pdf = await get_content_async(pdf_link)
    await save_pdf_async(pdf, path)
    
   
async def downloader_coro(f, args_list, concur_req):
    semaphore = asyncio.Semaphore(concur_req)
    to_do = [f(semaphore, args) for args in args_list]
    to_do_iter = tqdm.tqdm(asyncio.as_completed(to_do), total=len(to_do))
    
    res = []
    for future in to_do_iter:
        r = await future
        res.append(r)
        
    return res


async def get_links_and_names_on_one_page(semaphore, page_url):
    async with semaphore:
        html = await get_content_async(page_url)
    pdf_links_and_names = get_pdf_links_and_names(html)
    return pdf_links_and_names


@timer
def download_many():
    loop = asyncio.get_event_loop()
    
    # get pdf_links from page_urls
    urls = list(PAGE_URLS())[0:5]
    link_and_name_coro = downloader_coro(get_links_and_names_on_one_page, urls, MAX_CONCUR_REQ)
    pdf_links_and_names = loop.run_until_complete(link_and_name_coro)

    # get pdfs from pdf_links
    pdf_coro = downloader_coro(download_one_pdf, chain(*pdf_links_and_names), MAX_CONCUR_REQ)
    res = loop.run_until_complete(pdf_coro)
    count = len(res)
    
    loop.close()
    return count


if __name__ == '__main__':
    download_many()
