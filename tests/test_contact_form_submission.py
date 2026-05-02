from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_contact_form_submission(parabank: ParaBankPage):
    parabank.open_footer_link("Contact Us")

    parabank.submit_contact_form(
        name="Automation User",
        email="automation@example.com",
        phone="0501111111",
        message="Checking ParaBank contact flow from Playwright.",
    )
