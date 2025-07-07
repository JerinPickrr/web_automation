from ..config import config
import time

class BaseAction:
    """
    Base class for all actions. Implements retry logic.
    """
    def __init__(self, page):
        self.page = page

    def perform(self, *args, **kwargs):
        for attempt in range(config.RETRY_COUNT):
            try:
                return self._perform(*args, **kwargs)
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                time.sleep(config.RETRY_DELAY)
        raise Exception(f"Action failed after {config.RETRY_COUNT} attempts.")

    def _perform(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement _perform.")
