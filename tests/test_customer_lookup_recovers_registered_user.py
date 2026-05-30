from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_customer_lookup_recovers_registered_user(parabank: ParaBankPage, customer):
    parabank.register_from_home(customer)
    parabank.logout()

    parabank.open_lookup_from_home()
    parabank.recover_login_info(customer)
