from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
@pytest.mark.negative
def test_contact_form_required_fields(parabank: ParaBankPage):
    parabank.open_footer_link("Contact Us")
    parabank.submit_empty_contact_form()

    parabank.assert_contact_required_field_errors()
