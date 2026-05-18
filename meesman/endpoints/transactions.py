import httpx

from meesman.client import raise_for_response
from meesman.exceptions import MissingDataError
from meesman.models.base import ApiResponse
from meesman.models.order import (
    OrderBy,
    OrderByDirection,
    OrderTransaction,
    OrderTransactionsPage,
    OrderTransactionsRequest,
)

DEFAULT_TRANSACTIONS_ORDER_BY = [
    OrderBy(column="Date", direction=OrderByDirection.DESCENDING),
]


async def get_transactions_paginated(
    client: httpx.AsyncClient,
    registration_id: int,
    page: int = 1,
    order_by: list[OrderBy] | None = None,
) -> OrderTransactionsPage:
    body = OrderTransactionsRequest(
        page=page,
        order_by=order_by or DEFAULT_TRANSACTIONS_ORDER_BY,
    )
    response = await client.post(
        f"v1/orders/{registration_id}/transactions",
        json=body.model_dump(by_alias=True),
    )
    raise_for_response(response, "fetching order transactions")

    result = ApiResponse[OrderTransactionsPage].model_validate_json(response.content).data
    if result is None:
        raise MissingDataError("fetching order transactions")
    return result


async def get_transactions(
    client: httpx.AsyncClient,
    registration_id: int,
    order_by: list[OrderBy] | None = None,
) -> list[OrderTransaction]:
    all_rows: list[OrderTransaction] = []
    page = 1
    while True:
        result = await get_transactions_paginated(client, registration_id, page, order_by)
        if not result.rows:
            break

        all_rows.extend(result.rows)
        if len(all_rows) >= result.count:
            break
        page += 1

    return all_rows
