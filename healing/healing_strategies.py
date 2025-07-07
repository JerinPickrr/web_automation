class HealingStrategies:
    """
    Implements auto-healing strategies for failed actions.
    """
    def try_alternatives(self, page, alternatives):
        for selector in alternatives:
            try:
                if page.query_selector(selector):
                    return selector
            except Exception:
                continue
        return None
