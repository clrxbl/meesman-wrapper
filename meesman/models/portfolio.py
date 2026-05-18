from datetime import datetime
from enum import StrEnum

from meesman.models.base import ApiModel


class FundType(StrEnum):
    SAFE = "Safe"
    GROWTH = "Growth"


class Asset(ApiModel):
    fund_code: str | None = None
    name: str | None = None
    date_of_last_price: datetime | None = None
    number_of_units: float | None = None
    last_price: float | None = None
    total_value: float | None = None
    current_weight: float | None = None
    fund_type: FundType | None = None
    sort_order: int | None = None
    color: str | None = None
    info_url: str | None = None


class Portfolio(ApiModel):
    assets: list[Asset] | None = None
    amount_left_to_invest: float | None = None
    total_value: float | None = None
    total_percentage: float | None = None
    invested_start_date: datetime | None = None
