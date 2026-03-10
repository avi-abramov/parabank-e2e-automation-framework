from __future__ import annotations

from pathlib import Path
from time import sleep

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from src.core.settings import PROJECT_ROOT, Settings, get_settings


ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Browser:
    browser_type = getattr(playwright_instance, settings.browser_name, None)
    if browser_type is None:
        raise ValueError(
            f"Unsupported browser '{settings.browser_name}'. "
            "Use chromium, firefox, or webkit."
        )

    launch_options = {
        "headless": settings.headless,
        "slow_mo": settings.slow_mo_ms,
    }
    if settings.start_maximized and settings.browser_name == "chromium":
        launch_options["args"] = ["--start-maximized"]

    browser = browser_type.launch(
        **launch_options,
    )
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser, settings: Settings) -> BrowserContext:
    context_options = {
        "base_url": settings.base_url,
    }
    if settings.start_maximized and settings.browser_name == "chromium":
        context_options["no_viewport"] = True
    else:
        context_options["viewport"] = {
            "width": settings.viewport_width,
            "height": settings.viewport_height,
        }

    context = browser.new_context(**context_options)
    context.set_default_timeout(settings.default_timeout_ms)
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Page:
    page = context.new_page()
    yield page

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_name = f"{request.node.name}.png"
        page.screenshot(path=SCREENSHOTS_DIR / screenshot_name, full_page=True)

    settings = request.getfixturevalue("settings")
    if settings.test_pause_ms > 0:
        sleep(settings.test_pause_ms / 1000)

    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
