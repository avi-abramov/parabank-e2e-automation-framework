from __future__ import annotations

import pytest

from src.core.test_data import ParabankCustomer, build_parabank_customer
from src.pages.parabank_page import ParaBankPage


@pytest.fixture()
def parabank(page) -> ParaBankPage:
    app = ParaBankPage(page)
    app.open()
    return app


@pytest.fixture()
def customer() -> ParabankCustomer:
    return build_parabank_customer()
