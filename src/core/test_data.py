from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class ParabankCustomer:
    first_name: str
    last_name: str
    street: str
    city: str
    state: str
    zip_code: str
    phone: str
    ssn: str
    username: str
    password: str


@dataclass(frozen=True)
class BillPayDetails:
    name: str
    street: str
    city: str
    state: str
    zip_code: str
    phone: str
    account_number: str


def build_parabank_customer() -> ParabankCustomer:
    suffix = f"{datetime.now(UTC).strftime('%H%M%S')}{uuid4().hex[:4]}"

    return ParabankCustomer(
        first_name="Play",
        last_name="Writer",
        street="1 Test Street",
        city="Tel Aviv",
        state="Center",
        zip_code="12345",
        phone="0501234567",
        ssn=suffix,
        username=f"pw{suffix}",
        password="Pass123!",
    )


def build_updated_customer(customer: ParabankCustomer) -> ParabankCustomer:
    return replace(
        customer,
        street="99 Updated Street",
        city="Haifa",
        state="North",
        zip_code="30001",
        phone="0509990000",
    )


def build_bill_pay_details() -> BillPayDetails:
    suffix = datetime.now(UTC).strftime("%H%M%S")

    return BillPayDetails(
        name="Automation Payee",
        street="2 Billing Road",
        city="Ramat Gan",
        state="Center",
        zip_code="54321",
        phone="0507654321",
        account_number=f"98765{suffix}",
    )
