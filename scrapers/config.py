BASE_URL = "http://zfj.mee.gov.cn/jgjs/"
DEST_DIR = '../downloads/'


def PAGE_URLS():
    for i in range(1, 40):
        yield f"{BASE_URL}/index_{i}.shtml"