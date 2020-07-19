from concurrent import futures

from config import PAGE_URLS
from scraper import download_single_page, timer


@timer
def download_many():
    with futures.ThreadPoolExecutor(30) as executor:
        res = executor.map(download_single_page, list(PAGE_URLS()))
    print("All downloaded!")
    return len(list(res))
    
    
if __name__ == '__main__':
    download_many()
    

