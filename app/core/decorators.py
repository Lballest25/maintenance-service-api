import time
import functools
import logging

logger = logging.getLogger(__name__)


def measure_time(func):
    """
    Decorator to measure and log the execution time of a function.
    Works with both synchronous and asynchronous functions.
    """

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            return await func(*args, **kwargs)
        finally:
            elapsed_time = time.perf_counter() - start_time
            logger.info(
                "Function %s executed in %.4f seconds",
                func.__name__,
                elapsed_time,
            )

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_time = time.perf_counter() - start_time
            logger.info(
                "Function %s executed in %.4f seconds",
                func.__name__,
                elapsed_time,
            )

    return async_wrapper if hasattr(func, "__await__") else sync_wrapper
