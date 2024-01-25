import time

from log import logger


def timed(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.debug(f'Function {func.__name__!r} executed in {(end_time - start_time):.4f}s')
        return result

    return wrapper
