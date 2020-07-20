import os
import time

from scrapers.config import DEST_DIR


def gen_path(file_name):
    path = ''
    if '环境卫星' in file_name:
        path += '/环境卫星'
    elif '气象卫星' in file_name:
        path += '/气象卫星'
    else:
        return
    
    if '日报' in file_name:
        path += '/日报'
    elif '月报' in file_name:
        path += '/月报'
    else:
        return

    path = os.path.join(DEST_DIR + path, file_name + '.pdf')
    return path


def timer(f):
    def decorated(*args, **kwargs):
        t0 = time.time()
        count = f(*args, **kwargs)
        elapsed = time.time() - t0
        msg = "\n{} pages downloaded in {:.2f}s"
        print(msg.format(count, elapsed))
    return decorated