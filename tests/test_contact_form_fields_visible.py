from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_contact_form_fields_visible(parabank: ParaBankPage):
    parabank.open_footer_link("Contact Us")

    parabank.assert_contact_form_visible()
