from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def _default_base_url() -> str:
    return "https://parabank.parasoft.com/parabank/"


@dataclass(frozen=True)
class Settings:
    base_url: str = field(default_factory=lambda: os.getenv("BASE_URL", _default_base_url()))
    browser_name: str = field(default_factory=lambda: os.getenv("BROWSER", "chromium"))
    headless: bool = field(default_factory=lambda: _get_bool("HEADLESS", False))
    start_maximized: bool = field(default_factory=lambda: _get_bool("START_MAXIMIZED", True))
    slow_mo_ms: int = field(default_factory=lambda: _get_int("SLOW_MO_MS", 600))
    viewport_width: int = field(default_factory=lambda: _get_int("VIEWPORT_WIDTH", 1440))
    viewport_height: int = field(default_factory=lambda: _get_int("VIEWPORT_HEIGHT", 900))
    default_timeout_ms: int = field(default_factory=lambda: _get_int("DEFAULT_TIMEOUT_MS", 10000))
    test_pause_ms: int = field(default_factory=lambda: _get_int("TEST_PAUSE_MS", 5000))


def get_settings() -> Settings:
    return Settings()
