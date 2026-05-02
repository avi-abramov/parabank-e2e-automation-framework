from __future__ import annotations

import pytest

from src.core.test_data import build_parabank_customer
from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
@pytest.mark.negative
def test_duplicate_username_validation(parabank: ParaBankPage):
    customer = build_parabank_customer()

    parabank.open_registration_from_home()
    parabank.register_customer(customer)
    parabank.logout()

    parabank.open_registration_from_home()
    parabank.submit_registration(customer)

    parabank.assert_right_panel_contains("This username already exists.")
