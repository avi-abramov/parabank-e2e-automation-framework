from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_empty_login_requires_credentials(parabank: ParaBankPage):
    parabank.submit_empty_login()

    parabank.assert_empty_login_error()
