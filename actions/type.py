from .base_action import BaseAction

class TypeAction(BaseAction):
    """
    Types text into an element, with retry and healing logic.
    """
    def _perform(self, selector, text):
        self.page.fill(selector, text)

