from concurrent import futures

from scrapers.config import PAGE_URLS
from scrapers.scraper import download_single_page
from scrapers.utils import timer


@timer
def download_many():
    with futures.ThreadPoolExecutor(30) as executor:
        res = executor.map(download_single_page, list(PAGE_URLS()))
    print("All downloaded!")
    return len(list(res))
    
    
if __name__ == '__main__':
    download_many()
    

