from concurrent import futures

import tqdm

from scrapers.config import PAGE_URLS
from scrapers.scraper import download_single_page
from scrapers.utils import timer


@timer
def download_many():
    with futures.ThreadPoolExecutor(30) as executor:
        # codes almost equivalent to:
        # res = executor.map(download_single_page, PAGE_URLS())
        
        urls = list(PAGE_URLS())[0:10]
        to_do = []
        for url in urls:
            future = executor.submit(download_single_page, url)
            to_do.append(future)
        
        res = []
        done_iter = tqdm.tqdm(futures.as_completed(to_do), total=len(urls))
        for future in done_iter:
            r = future.result()
            res.append(r)
        
    print("All downloaded!")
    print(res)
    return len(list(res))
    
    
if __name__ == '__main__':
    download_many()
    

