import sys
import time
import asyncio
import itertools


def timer(f):
    def decorated(*args, **kwargs):
        t0 = time.time()
        count = f(*args, **kwargs)
        elapsed = time.time() - t0
        msg = "\n downloaded {} in {:.2f}s"
        print(msg.format(count, elapsed))
    return decorated


async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))