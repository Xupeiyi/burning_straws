import time
from config import PAGE_URLS
from scraper import download_single_page


def timer(f):
    def decorated(*args, **kwargs):
        t0 = time.time()
        count = f(*args, **kwargs)
        elapsed = time.time() - t0
        msg = "\n{} pages downloaded in {:.2f}s"
        print(msg.format(count, elapsed))
    return decorated


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
    
    

