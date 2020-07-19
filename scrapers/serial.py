import time
from config import PAGE_URLS
from scraper import download_single_page, timer


@timer
def download_many():
    count = 0
    for url in PAGE_URLS():
        download_single_page(url)
        count += 1
    print("All downloaded!")
    return count
    
    
if __name__ == '__main__':
    download_many()
    
    

