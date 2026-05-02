from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.fixture()
def parabank(page) -> ParaBankPage:
    app = ParaBankPage(page)
    app.open()
    return app

