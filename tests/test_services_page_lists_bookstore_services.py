from __future__ import annotations

import pytest

from src.pages.parabank_page import ParaBankPage


@pytest.mark.e2e
def test_services_page_lists_bookstore_services(parabank: ParaBankPage):
    parabank.open_header_link("Services")

    parabank.assert_right_panel_contains("Available Bookstore SOAP services")
