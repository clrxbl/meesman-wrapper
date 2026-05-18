import json
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import field_validator

from meesman.models.base import ApiModel
from meesman.models.trade import TradeItem


class OrderByDirection(StrEnum):
    ASCENDING = "Ascending"
    DESCENDING = "Descending"


class OrderBy(ApiModel):
    column: str
    direction: OrderByDirection


class FrequencyType(StrEnum):
    ONCE = "Once"
    PERIODIC = "Periodic"


class OrderType(StrEnum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    REBALANCE = "Rebalance"
    PERIODIC_DEPOSIT = "PeriodicDeposit"
    PERIODIC_WITHDRAWAL = "PeriodicWithdrawal"
    SWITCH = "Switch"
    REFUND = "Refund"


class OrderBaseType(StrEnum):
    BUY = "Buy"
    SELL = "Sell"
    INDIRECT_SWITCH = "IndirectSwitch"
    SWITCH = "Switch"
    PRO_RATA = "ProRata"
    RE_INVEST = "ReInvest"
    REFUND = "Refund"
    ASSET_MIX = "AssetMix"
    REBALANCE = "Rebalance"
    CORRECTION = "Correction"
    INTERNAL_SWITCH = "InternalSwitch"
    PERIODICAL_SELL = "PeriodicalSell"
    PERIODICAL_BUY = "PeriodicalBuy"
    WITHDRAW_DEPOSIT_SELL = "WithdrawDepositSell"
    WITHDRAW_DEPOSIT_BUY = "WithdrawDepositBuy"
    SWITCH_SELL = "SwitchSell"
    SWITCH_BUY = "SwitchBuy"


class PaymentMethod(StrEnum):
    TIKKIE = "Tikkie"
    MANUAL = "Manual"
    DIRECT_DEBIT = "DirectDebit"
    IDEAL = "IDeal"


class OrderPlacementType(StrEnum):
    EURO = "Euro"
    PARTICIPATION = "Participation"


class OrderTransaction(ApiModel):
    id: UUID | None = None
    pengine_id: UUID | None = None
    registration_id: int | None = None
    frequency: FrequencyType | None = None
    type: OrderType | None = None
    order_base_type: OrderBaseType | None = None
    payment_method: PaymentMethod | None = None
    use_fund_mix: bool | None = None
    date_created: datetime | None = None
    collection_date: datetime | None = None
    date_executed: datetime | None = None
    fund: str | None = None
    amount: float | None = None
    number_of_units: float | None = None
    order_placement_type: OrderPlacementType | None = None
    cut_off_on_at: datetime | None = None
    cut_off_time_passed: bool | None = None
    trade_items: list[TradeItem] | None = None


class OrderTransactionsRequest(ApiModel):
    page: int
    order_by: list[OrderBy]
    page_size: int = 15  # Default page size used by the Meesman app, do not change


class OrderTransactionsPage(ApiModel):
    # The API returns "rows" as a JSON-encoded string rather than a JSON array
    rows: list[OrderTransaction] = []
    count: int = 0
    silicon_message_list: list[Any] | None = None

    @field_validator("rows", mode="before")
    @classmethod
    def _parse_rows(cls, v: Any) -> Any:
        return json.loads(v) if isinstance(v, str) else v
