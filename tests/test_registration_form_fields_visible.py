from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_registration_form_fields_visible(parabank: ParaBankPage):
    parabank.open_registration_from_home()

    parabank.assert_registration_form_visible()
