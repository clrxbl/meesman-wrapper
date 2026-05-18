from datetime import datetime

from meesman.models.base import ApiModel


class Yield(ApiModel):
    year: int | None = None
    start_value: float | None = None
    deposits: float | None = None
    withdrawals: float | None = None
    fund_costs: float | None = None
    transaction_costs: float | None = None
    end_value: float | None = None
    year_return: float | None = None
    return_on_entire_period: float | None = None


class YieldChart(ApiModel):
    date: datetime | None = None
    deposit: float | None = None
    value: float | None = None
