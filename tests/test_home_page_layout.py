from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_home_page_layout(parabank: ParaBankPage):
    parabank.assert_home_page_layout()
