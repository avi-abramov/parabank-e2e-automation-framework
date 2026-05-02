from __future__ import annotations

from datetime import date
from decimal import Decimal

from playwright.sync_api import expect

from src.core.test_data import BillPayDetails, ParabankCustomer
from src.pages.base_page import BasePage


class ParaBankPage(BasePage):
    INTERNAL_ERROR_TEXT = "An internal error has occurred and has been logged."

    def open(self) -> None:
        self.goto("index.htm")
        expect(self.page).to_have_title("ParaBank | Welcome | Online Banking")
        expect(self.locator("#loginPanel")).to_be_visible()

    def assert_no_internal_error(self) -> None:
        expect(self.locator("#rightPanel")).not_to_contain_text(self.INTERNAL_ERROR_TEXT)

    def open_header_link(self, link_name: str) -> None:
        self.locator("#headerPanel").get_by_role("link", name=link_name).click()

    def open_footer_link(self, link_name: str) -> None:
        self.locator("#footerPanel").get_by_role("link", name=link_name).click()

    def open_registration_from_home(self) -> None:
        self.locator("#loginPanel").get_by_role("link", name="Register").click()
        expect(self.locator("#rightPanel")).to_contain_text("Signing up is easy!")
        self.assert_no_internal_error()

    def open_lookup_from_home(self) -> None:
        self.locator("#loginPanel").get_by_role("link", name="Forgot login info?").click()
        expect(self.locator("#rightPanel")).to_contain_text("Customer Lookup")
        self.assert_no_internal_error()

    def assert_home_page_layout(self) -> None:
        self.assert_no_internal_error()
        expect(self.locator("#leftPanel")).to_contain_text("Customer Login")
        expect(self.locator("#loginPanel")).to_contain_text("Username")
        expect(self.locator("#loginPanel")).to_contain_text("Password")
        expect(self.locator("#headerPanel")).to_contain_text("About Us")
        expect(self.locator("#headerPanel")).to_contain_text("Services")
        expect(self.locator("#headerPanel")).to_contain_text("Products")
        expect(self.locator("#headerPanel")).to_contain_text("Locations")
        expect(self.locator("#headerPanel")).to_contain_text("Admin Page")
        expect(self.locator("#footerPanel")).to_contain_text("Home")
        expect(self.locator("#footerPanel")).to_contain_text("Site Map")
        expect(self.locator("#footerPanel")).to_contain_text("Contact Us")

    def assert_contact_form_visible(self) -> None:
        self.assert_no_internal_error()
        expect(self.locator("input[id='name']")).to_be_visible()
        expect(self.locator("input[id='email']")).to_be_visible()
        expect(self.locator("input[id='phone']")).to_be_visible()
        expect(self.locator("textarea[id='message']")).to_be_visible()
        expect(self.page.get_by_role("button", name="Send to Customer Care")).to_be_visible()

    def assert_registration_form_visible(self) -> None:
        self.assert_no_internal_error()
        field_ids = [
            "customer.firstName",
            "customer.lastName",
            "customer.address.street",
            "customer.address.city",
            "customer.address.state",
            "customer.address.zipCode",
            "customer.phoneNumber",
            "customer.ssn",
            "customer.username",
            "customer.password",
            "repeatedPassword",
        ]
        for field_id in field_ids:
            expect(self.locator(f"input[id='{field_id}']")).to_be_visible()
        expect(self.page.get_by_role("button", name="Register")).to_be_visible()

    def assert_customer_lookup_form_visible(self) -> None:
        self.assert_no_internal_error()
        field_ids = [
            "firstName",
            "lastName",
            "address\\.street",
            "address\\.city",
            "address\\.state",
            "address\\.zipCode",
            "ssn",
        ]
        for field_id in field_ids:
            expect(self.locator(f"#{field_id}")).to_be_visible()
        expect(self.page.get_by_role("button", name="Find My Login Info")).to_be_visible()

    def assert_right_panel_contains(self, *texts: str) -> None:
        self.assert_no_internal_error()
        panel = self.locator("#rightPanel")
        for text in texts:
            expect(panel).to_contain_text(text)

    def submit_contact_form(
        self,
        *,
        name: str,
        email: str,
        phone: str,
        message: str,
    ) -> None:
        self.locator("input[id='name']").fill(name)
        self.locator("input[id='email']").fill(email)
        self.locator("input[id='phone']").fill(phone)
        self.locator("textarea[id='message']").fill(message)
        self.page.get_by_role("button", name="Send to Customer Care").click()
        self.assert_right_panel_contains(f"Thank you {name}")
        self.assert_right_panel_contains("A Customer Care Representative will be contacting you.")

    def submit_empty_contact_form(self) -> None:
        self.page.get_by_role("button", name="Send to Customer Care").click()

    def assert_contact_required_field_errors(self) -> None:
        self.assert_right_panel_contains(
            "Name is required.",
            "Email is required.",
            "Phone is required.",
            "Message is required.",
        )

    def _fill_registration_form(self, customer: ParabankCustomer) -> None:
        values = {
            "customer.firstName": customer.first_name,
            "customer.lastName": customer.last_name,
            "customer.address.street": customer.street,
            "customer.address.city": customer.city,
            "customer.address.state": customer.state,
            "customer.address.zipCode": customer.zip_code,
            "customer.phoneNumber": customer.phone,
            "customer.ssn": customer.ssn,
            "customer.username": customer.username,
            "customer.password": customer.password,
            "repeatedPassword": customer.password,
        }

        for field_id, value in values.items():
            self.locator(f"input[id='{field_id}']").fill(value)

    def submit_registration(self, customer: ParabankCustomer) -> None:
        self._fill_registration_form(customer)
        self.page.get_by_role("button", name="Register").click()

    def submit_empty_registration(self) -> None:
        self.page.get_by_role("button", name="Register").click()

    def assert_registration_required_field_errors(self) -> None:
        self.assert_right_panel_contains(
            "First name is required.",
            "Last name is required.",
            "Address is required.",
            "City is required.",
            "State is required.",
            "Zip Code is required.",
            "Social Security Number is required.",
            "Username is required.",
            "Password is required.",
            "Password confirmation is required.",
        )

    def register_customer(self, customer: ParabankCustomer) -> None:
        self.submit_registration(customer)
        self.assert_right_panel_contains(f"Welcome {customer.username}")
        self.assert_right_panel_contains("Your account was created successfully.")
        expect(self.locator("#leftPanel")).to_contain_text("Open New Account")

    def attempt_login(self, username: str, password: str) -> None:
        self.locator("input[name='username']").fill(username)
        self.locator("input[name='password']").fill(password)
        self.page.get_by_role("button", name="Log In").click()

    def submit_empty_login(self) -> None:
        self.page.get_by_role("button", name="Log In").click()

    def login(self, username: str, password: str) -> None:
        self.attempt_login(username, password)
        expect(self.locator("#leftPanel")).to_contain_text("Accounts Overview")
        self.assert_no_internal_error()

    def assert_login_error(self) -> None:
        self.assert_right_panel_contains("Error!")
        self.assert_right_panel_contains("The username and password could not be verified.")

    def assert_empty_login_error(self) -> None:
        self.assert_right_panel_contains("Error!")
        self.assert_right_panel_contains("Please enter a username and password.")

    def logout(self) -> None:
        self.locator("#leftPanel").get_by_role("link", name="Log Out").click()
        expect(self.locator("#loginPanel")).to_be_visible()

    def open_accounts_overview(self) -> None:
        self.locator("#leftPanel").get_by_role("link", name="Accounts Overview").click()
        expect(self.locator("#accountTable")).to_be_visible()
        self.assert_no_internal_error()

    def get_account_numbers(self) -> list[str]:
        self.open_accounts_overview()
        account_links = self.locator("#accountTable a")
        expect(account_links.first).to_be_visible()
        return [text.strip() for text in account_links.all_inner_texts() if text.strip()]

    def open_account_details(self, account_id: str) -> str:
        self.open_accounts_overview()
        self.locator("#accountTable a").filter(has_text=account_id).first.click()
        self.assert_right_panel_contains("Account Details")
        self.page.wait_for_function(
            "(expectedAccountId) => document.querySelector('#rightPanel')?.innerText.includes(expectedAccountId)",
            arg=account_id,
        )
        return self.locator("#rightPanel").inner_text()

    def filter_account_activity_by_type(self, transaction_type: str) -> str:
        self.locator("#transactionType").select_option(label=transaction_type)
        self.page.get_by_role("button", name="Go").click()
        expect(self.locator("#transactionTable")).to_be_visible()
        return self.locator("#transactionTable").inner_text()

    def open_new_account(self, *, from_account_id: str, account_type: str = "SAVINGS") -> str:
        self.locator("#leftPanel").get_by_role("link", name="Open New Account").click()
        self.locator("#type").select_option(label=account_type)
        self.locator("#fromAccountId").select_option(value=from_account_id)
        self.page.get_by_role("button", name="Open New Account").click()
        self.assert_right_panel_contains("Account Opened!")
        self.page.wait_for_function(
            "document.querySelector('#newAccountId') && "
            "document.querySelector('#newAccountId').textContent.trim().length > 0"
        )
        return self.locator("#newAccountId").text_content().strip()

    def transfer_funds(self, *, amount: Decimal, from_account_id: str, to_account_id: str) -> None:
        self.locator("#leftPanel").get_by_role("link", name="Transfer Funds").click()
        self.locator("#amount").fill(str(amount))
        self.locator("#fromAccountId").select_option(value=from_account_id)
        self.locator("#toAccountId").select_option(value=to_account_id)
        self.page.get_by_role("button", name="Transfer").click()
        self.assert_right_panel_contains("Transfer Complete!")
        self.assert_right_panel_contains("See Account Activity for more details.")

    def open_bill_pay_page(self) -> None:
        self.locator("#leftPanel").get_by_role("link", name="Bill Pay").click()
        self.assert_right_panel_contains("Bill Payment Service")

    def pay_bill(self, *, payee: BillPayDetails, amount: Decimal, from_account_id: str) -> None:
        self.open_bill_pay_page()

        values = {
            "payee.name": payee.name,
            "payee.address.street": payee.street,
            "payee.address.city": payee.city,
            "payee.address.state": payee.state,
            "payee.address.zipCode": payee.zip_code,
            "payee.phoneNumber": payee.phone,
            "payee.accountNumber": payee.account_number,
            "verifyAccount": payee.account_number,
            "amount": str(amount),
        }

        for field_name, value in values.items():
            self.locator(f"input[name='{field_name}']").fill(value)

        self.locator("select[name='fromAccountId']").select_option(value=from_account_id)
        self.page.get_by_role("button", name="Send Payment").click()
        self.assert_right_panel_contains("Bill Payment Complete")
        self.assert_right_panel_contains("See Account Activity for more details.")

    def submit_empty_bill_payment(self) -> None:
        self.page.get_by_role("button", name="Send Payment").click()

    def assert_bill_payment_required_field_errors(self) -> None:
        self.assert_right_panel_contains(
            "Payee name is required.",
            "Address is required.",
            "City is required.",
            "State is required.",
            "Zip Code is required.",
            "Phone number is required.",
            "Account number is required.",
            "The amount cannot be empty.",
        )

    def find_transactions_by_date(self, *, account_id: str, on_date: date) -> str:
        self.locator("#leftPanel").get_by_role("link", name="Find Transactions").click()
        self.locator("#accountId").select_option(value=account_id)
        self.locator("#transactionDate").fill(on_date.strftime("%m-%d-%Y"))
        self.locator("#findByDate").click()
        expect(self.locator("#transactionTable")).to_be_visible()
        return self.locator("#transactionTable").inner_text()

    def find_transactions_by_amount(self, *, account_id: str, amount: Decimal) -> str:
        self.locator("#leftPanel").get_by_role("link", name="Find Transactions").click()
        self.locator("#accountId").select_option(value=account_id)
        self.locator("#amount").fill(str(amount))
        self.locator("#findByAmount").click()
        expect(self.locator("#transactionTable")).to_be_visible()
        return self.locator("#transactionTable").inner_text()

    def find_transactions_by_date_range(
        self,
        *,
        account_id: str,
        from_date: date,
        to_date: date,
    ) -> str:
        self.locator("#leftPanel").get_by_role("link", name="Find Transactions").click()
        self.locator("#accountId").select_option(value=account_id)
        self.locator("#fromDate").fill(from_date.strftime("%m-%d-%Y"))
        self.locator("#toDate").fill(to_date.strftime("%m-%d-%Y"))
        self.locator("#findByDateRange").click()
        expect(self.locator("#transactionTable")).to_be_visible()
        return self.locator("#transactionTable").inner_text()

    def update_contact_info(self, customer: ParabankCustomer) -> None:
        self.locator("#leftPanel").get_by_role("link", name="Update Contact Info").click()

        values = {
            "customer.firstName": customer.first_name,
            "customer.lastName": customer.last_name,
            "customer.address.street": customer.street,
            "customer.address.city": customer.city,
            "customer.address.state": customer.state,
            "customer.address.zipCode": customer.zip_code,
            "customer.phoneNumber": customer.phone,
        }

        for field_id, value in values.items():
            self.locator(f"input[id='{field_id}']").fill(value)

        self.page.get_by_role("button", name="Update Profile").click()
        self.assert_right_panel_contains("Profile Updated")
        self.assert_right_panel_contains("Your updated address and phone number have been added to the system.")

    def request_loan(self, *, amount: Decimal, down_payment: Decimal, from_account_id: str) -> None:
        self.locator("#leftPanel").get_by_role("link", name="Request Loan").click()
        self.locator("#amount").fill(str(amount))
        self.locator("#downPayment").fill(str(down_payment))
        self.locator("#fromAccountId").select_option(value=from_account_id)
        self.page.get_by_role("button", name="Apply Now").click()
        self.assert_right_panel_contains("Loan Request Processed")
        self.assert_right_panel_contains("approved")

    def submit_customer_lookup(self, customer: ParabankCustomer) -> None:
        self.locator("#firstName").fill(customer.first_name)
        self.locator("#lastName").fill(customer.last_name)
        self.locator("#address\\.street").fill(customer.street)
        self.locator("#address\\.city").fill(customer.city)
        self.locator("#address\\.state").fill(customer.state)
        self.locator("#address\\.zipCode").fill(customer.zip_code)
        self.locator("#ssn").fill(customer.ssn)
        self.page.get_by_role("button", name="Find My Login Info").click()

    def recover_login_info(self, customer: ParabankCustomer) -> None:
        self.submit_customer_lookup(customer)
        self.assert_right_panel_contains("Your login information was located successfully.")
        self.assert_right_panel_contains(f"Username: {customer.username}")
        self.assert_right_panel_contains(f"Password: {customer.password}")

    def assert_customer_lookup_error(self) -> None:
        self.assert_right_panel_contains("Error!")
        self.assert_right_panel_contains("The customer information provided could not be found.")
