from __future__ import annotations

import pytest

from src.core.test_data import build_parabank_customer
from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_customer_lookup_failure(parabank: ParaBankPage):
    missing_customer = build_parabank_customer()

    parabank.open_lookup_from_home()
    parabank.submit_customer_lookup(missing_customer)

    parabank.assert_customer_lookup_error()
