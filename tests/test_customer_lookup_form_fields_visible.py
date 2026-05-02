from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_customer_lookup_form_fields_visible(parabank: ParaBankPage):
    parabank.open_lookup_from_home()

    parabank.assert_customer_lookup_form_visible()
