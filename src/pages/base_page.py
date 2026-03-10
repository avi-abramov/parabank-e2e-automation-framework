from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, path: str = "/") -> None:
        self.page.goto(path)

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def assert_title_contains(self, value: str) -> None:
        expect(self.page).to_have_title(value)

