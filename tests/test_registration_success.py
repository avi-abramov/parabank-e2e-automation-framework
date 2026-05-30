from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_registration_success(parabank: ParaBankPage, customer):
    parabank.register_from_home(customer)
