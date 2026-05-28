from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pytest

from src.core.settings import PROJECT_ROOT, Settings


ALLURE_RESULTS_DIR = PROJECT_ROOT / "allure-results"

try:
    import allure
except ImportError:  # pragma: no cover - fallback keeps pytest usable before install.
    allure = None


@contextmanager
def report_step(title: str) -> Iterator[None]:
    if allure is None:
        yield
        return

    with allure.step(title):
        yield


def attach_png(path: Path, name: str) -> None:
    if allure is None or not path.exists():
        return

    allure.attach.file(
        str(path),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


def attach_text(name: str, body: str) -> None:
    if allure is None:
        return

    allure.attach(
        body,
        name=name,
        attachment_type=allure.attachment_type.TEXT,
    )


def apply_test_metadata(item: pytest.Item) -> None:
    if allure is None:
        return

    test_name = item.name.replace("_", " ").title()
    feature = _feature_for_test(item.name)

    allure.dynamic.epic("ParaBank UI Automation")
    allure.dynamic.feature(feature)
    allure.dynamic.story("Negative validation" if item.get_closest_marker("negative") else "Positive user journey")
    allure.dynamic.title(test_name)


def write_allure_environment(settings: Settings) -> None:
    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    environment = {
        "Project": "ParaBank E2E Automation Framework",
        "Base URL": settings.base_url,
        "Browser": settings.browser_name,
        "Headless": str(settings.headless),
        "Start Maximized": str(settings.start_maximized),
        "Slow Motion MS": str(settings.slow_mo_ms),
        "Test Pause MS": str(settings.test_pause_ms),
    }

    lines = [f"{key}={value}" for key, value in environment.items()]
    (ALLURE_RESULTS_DIR / "environment.properties").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_allure_categories() -> None:
    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    categories = [
        {
            "name": "ParaBank Internal Server Error",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*An internal error has occurred and has been logged.*",
        },
        {
            "name": "UI Assertion Failure",
            "matchedStatuses": ["failed"],
            "traceRegex": ".*AssertionError.*",
        },
        {
            "name": "Timeout",
            "matchedStatuses": ["failed", "broken"],
            "messageRegex": ".*Timeout.*",
        },
    ]

    (ALLURE_RESULTS_DIR / "categories.json").write_text(
        json.dumps(categories, indent=2),
        encoding="utf-8",
    )


def _feature_for_test(test_name: str) -> str:
    if "contact" in test_name:
        return "Contact"
    if "registration" in test_name or "duplicate_username" in test_name:
        return "Registration"
    if "lookup" in test_name:
        return "Customer Lookup"
    if "login" in test_name:
        return "Login"
    if "services" in test_name or "site_map" in test_name or "about" in test_name:
        return "Public Navigation"
    return "Home Page"
