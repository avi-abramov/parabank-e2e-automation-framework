from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
@pytest.mark.negative
def test_customer_lookup_failure(parabank: ParaBankPage, customer):
    parabank.open_lookup_from_home()
    parabank.submit_customer_lookup(customer)

    parabank.assert_customer_lookup_error()
