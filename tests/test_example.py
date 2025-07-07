# Requires: pip install pytest playwright
import pytest
from playwright.sync_api import sync_playwright
from web_automation.actions.click import ClickAction
from web_automation.actions.type import TypeAction

def test_example():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://example.com')
        click = ClickAction(page)
        type_ = TypeAction(page)
        # Example usage (selectors are placeholders)
        # type_.perform('input[name="q"]', 'web automation')
        # click.perform('button[type="submit"]')
        browser.close()
