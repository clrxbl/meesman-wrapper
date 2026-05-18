from datetime import datetime
from enum import StrEnum

from meesman.models.base import ApiModel


class TradeItemTradeType(StrEnum):
    BUY = "Buy"
    SELL = "Sell"


class TradeItemExecutionType(StrEnum):
    VALUE_BASED = "ValueBased"
    UNIT_BASED = "UnitBased"


class TradeItemTradeStatus(StrEnum):
    CREATED = "Created"
    RESERVE_FOR_ORDER = "ReserveForOrder"
    NO_CASH_AVAILABLE = "NoCashAvailable"
    PENDING = "Pending"
    CUTOFF_TIME_PASSED = "CutoffTimePassed"
    LOCKED_FOR_PROCESS = "LockedForProcess"
    WAITING_FOR_COSTS_CALCULATED = "WaitingForCostsCalculated"
    WAITING_FOR_PORTFOLIO = "WaitingForPortfolio"
    WAITING_FOR_TRADE = "WaitingForTrade"
    PROCESSED = "Processed"
    CANCELLED = "Cancelled"
    READY_FOR_PAYOUT = "ReadyForPayout"
    REVERSED = "Reversed"


class TradeItem(ApiModel):
    fund: str | None = None
    market_date: datetime | None = None
    trade_type: TradeItemTradeType | None = None
    execution_type: TradeItemExecutionType | None = None
    units_of_asset: float | None = None
    net_value: float | None = None
    gross_value: float | None = None
    charged_costs: float | None = None
    status: TradeItemTradeStatus | None = None
    stock_price: float | None = None
    type_as_string: str | None = None
