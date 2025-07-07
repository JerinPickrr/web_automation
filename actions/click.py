from .base_action import BaseAction

class ClickAction(BaseAction):
    """
    Clicks an element, with retry and healing logic.
    """
    def _perform(self, selector):
        self.page.click(selector)
