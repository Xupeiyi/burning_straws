import time


def timer(f):
    def decorated(*args, **kwargs):
        t0 = time.time()
        count = f(*args, **kwargs)
        elapsed = time.time() - t0
        msg = "\n{} pages downloaded in {:.2f}s"
        print(msg.format(count, elapsed))
    return decorated
