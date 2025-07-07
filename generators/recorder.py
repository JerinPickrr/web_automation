class Recorder:
    """
    Records user actions for auto test case generation.
    """
    def __init__(self):
        self.actions = []

    def record_action(self, action, selector, value=None):
        self.actions.append({
            'action': action,
            'selector': selector,
            'value': value
        })

    def export(self):
        return self.actions
