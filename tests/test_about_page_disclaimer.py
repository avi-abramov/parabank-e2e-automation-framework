from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_about_page_disclaimer(parabank: ParaBankPage):
    parabank.open_header_link("About Us")

    parabank.assert_right_panel_contains("ParaSoft Demo Website", "ParaBank is not a real bank!")
