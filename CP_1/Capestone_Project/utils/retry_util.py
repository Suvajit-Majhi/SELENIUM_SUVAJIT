"""
retry_util.py
-------------
Hand-written retry decorator with exponential backoff. Deliberately
NOT using pytest-rerunfailures -- the point is to show *why* a UI
step is flaky (StaleElementReference, ElementClickIntercepted,
TimeoutException) and retry only the operation itself, with backoff,
rather than re-running the whole test from scratch.

Usage:
    from utils.retry_util import retry

    @retry(exceptions=(StaleElementReferenceException, TimeoutException))
    def click_login_button(self):
        ...
"""

import time
from functools import wraps

from config.config_loader import settings
from utils.logger import get_logger

log = get_logger(__name__)


def retry(exceptions=(Exception,), max_attempts: int = None, base_delay: float = None, backoff: float = None):
    """
    Decorator that retries the wrapped function on the given exception
    types, with exponential backoff.

    max_attempts / base_delay / backoff default to the values in
    config.yaml's `retry:` section, but can be overridden per-call.
    """
    cfg = settings.retry
    max_attempts = max_attempts or cfg.max_attempts
    base_delay = base_delay if base_delay is not None else cfg.base_delay_seconds
    backoff = backoff if backoff is not None else cfg.backoff_multiplier

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            delay = base_delay
            last_exception = None

            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    log.warning(
                        f"[retry] '{func.__name__}' failed on attempt {attempt}/{max_attempts} "
                        f"with {type(e).__name__}: {e}"
                    )
                    if attempt == max_attempts:
                        break
                    time.sleep(delay)
                    delay *= backoff
                    attempt += 1

            log.error(f"[retry] '{func.__name__}' exhausted {max_attempts} attempts. Raising last exception.")
            raise last_exception

        return wrapper

    return decorator
