from enum import StrEnum

from meesman.models.base import ApiModel


class RegistrationType(StrEnum):
    ONE_PERSON = "OnePerson"
    TWO_PERSONS = "TwoPersons"
    CHILD = "Child"
    COMPANY = "Company"
    RETIREMENT = "Retirement"
    EMPLOYER = "Employer"


class Registration(ApiModel):
    registration_id: int | None = None
    investment_account_number: str | None = None
    account_holders: str | None = None
    customer_label: str | None = None
    type: RegistrationType | None = None
    has_fund_mix: bool | None = None
    value: float | None = None
    silicon_entity_tags: str | None = None
    has_asset_management_tag: bool | None = None
    status: str | None = None
    is_read_only: bool | None = None
    is_linked_to_employer: bool | None = None
    has_outstanding_actions: bool | None = None
