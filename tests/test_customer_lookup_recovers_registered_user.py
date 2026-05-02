from __future__ import annotations

import pytest

from src.core.test_data import build_parabank_customer
from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_customer_lookup_recovers_registered_user(parabank: ParaBankPage):
    customer = build_parabank_customer()

    parabank.open_registration_from_home()
    parabank.register_customer(customer)
    parabank.logout()

    parabank.open_lookup_from_home()
    parabank.recover_login_info(customer)
