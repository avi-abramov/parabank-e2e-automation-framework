from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from src.core.test_data import (
    build_bill_pay_details,
    build_parabank_customer,
    build_updated_customer,
)
from src.pages.parabank_page import ParaBankPage


@pytest.fixture()
def parabank(page) -> ParaBankPage:
    app = ParaBankPage(page)
    app.open()
    return app


@pytest.mark.e2e
def test_public_navigation_and_contact_form(parabank: ParaBankPage):
    parabank.open_header_link("About Us")
    parabank.assert_right_panel_contains("ParaSoft Demo Website", "ParaBank is not a real bank!")

    parabank.open()
    parabank.open_header_link("Services")
    parabank.assert_right_panel_contains("Available Bookstore SOAP services")

    parabank.open()
    parabank.open_footer_link("Site Map")
    parabank.assert_right_panel_contains("Account Services", "Request Loan")

    parabank.open()
    parabank.open_footer_link("Contact Us")
    parabank.submit_contact_form(
        name="Automation User",
        email="automation@example.com",
        phone="0501111111",
        message="Checking ParaBank contact flow from Playwright.",
    )


@pytest.mark.e2e
def test_registration_login_logout_and_customer_lookup(parabank: ParaBankPage):
    customer = build_parabank_customer()

    parabank.open_registration_from_home()
    parabank.register_customer(customer)
    parabank.logout()

    parabank.login(customer.username, customer.password)
    parabank.logout()

    parabank.open_lookup_from_home()
    parabank.recover_login_info(customer)


@pytest.mark.e2e
def test_negative_login_duplicate_username_and_lookup_errors(parabank: ParaBankPage):
    missing_customer = build_parabank_customer()
    parabank.attempt_login("invalid-user", "invalid-pass")
    parabank.assert_login_error()

    parabank.open()
    customer = build_parabank_customer()
    parabank.open_registration_from_home()
    parabank.register_customer(customer)
    parabank.logout()

    parabank.open_registration_from_home()
    parabank.submit_registration(customer)
    parabank.assert_right_panel_contains("This username already exists.")

    parabank.open()
    parabank.open_lookup_from_home()
    parabank.submit_customer_lookup(missing_customer)
    parabank.assert_customer_lookup_error()


@pytest.mark.e2e
def test_open_new_account_and_transfer_funds(parabank: ParaBankPage):
    customer = build_parabank_customer()

    parabank.open_registration_from_home()
    parabank.register_customer(customer)

    primary_account = parabank.get_account_numbers()[0]
    savings_account = parabank.open_new_account(from_account_id=primary_account)

    assert savings_account != primary_account

    accounts_after_open = parabank.get_account_numbers()
    assert primary_account in accounts_after_open
    assert savings_account in accounts_after_open

    parabank.transfer_funds(
        amount=Decimal("250"),
        from_account_id=primary_account,
        to_account_id=savings_account,
    )


@pytest.mark.e2e
def test_account_details_show_transfer_history(parabank: ParaBankPage):
    customer = build_parabank_customer()

    parabank.open_registration_from_home()
    parabank.register_customer(customer)

    primary_account = parabank.get_account_numbers()[0]
    savings_account = parabank.open_new_account(from_account_id=primary_account)
    parabank.transfer_funds(
        amount=Decimal("250"),
        from_account_id=primary_account,
        to_account_id=savings_account,
    )

    account_details = parabank.open_account_details(primary_account)
    assert "Funds Transfer Sent" in account_details
    assert "$250.00" in account_details
    assert primary_account in account_details


@pytest.mark.e2e
def test_bill_pay_transactions_profile_update_loan_and_logout(parabank: ParaBankPage):
    customer = build_parabank_customer()
    updated_customer = build_updated_customer(customer)
    payee = build_bill_pay_details()

    parabank.open_registration_from_home()
    parabank.register_customer(customer)

    primary_account = parabank.get_account_numbers()[0]

    parabank.pay_bill(
        payee=payee,
        amount=Decimal("35"),
        from_account_id=primary_account,
    )

    parabank.update_contact_info(updated_customer)
    parabank.request_loan(
        amount=Decimal("500"),
        down_payment=Decimal("100"),
        from_account_id=primary_account,
    )

    transactions = parabank.find_transactions_by_date(
        account_id=primary_account,
        on_date=date.today(),
    )
    assert "Down Payment for Loan" in transactions
    assert "$100.00" in transactions

    parabank.logout()

    parabank.open_lookup_from_home()
    parabank.recover_login_info(updated_customer)
