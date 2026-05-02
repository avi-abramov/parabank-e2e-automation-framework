from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_site_map_lists_account_services(parabank: ParaBankPage):
    parabank.open_footer_link("Site Map")

    parabank.assert_right_panel_contains("Account Services", "Request Loan")
