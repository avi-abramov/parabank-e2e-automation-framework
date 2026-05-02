from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_registration_required_fields(parabank: ParaBankPage):
    parabank.open_registration_from_home()
    parabank.submit_empty_registration()

    parabank.assert_registration_required_field_errors()

