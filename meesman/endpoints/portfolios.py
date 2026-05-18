import httpx

from meesman.client import raise_for_response
from meesman.exceptions import MissingDataError
from meesman.models.base import ApiResponse
from meesman.models.portfolio import Portfolio


async def get_portfolio(client: httpx.AsyncClient, registration_id: int) -> Portfolio:
    response = await client.get(f"v1/portfolios/{registration_id}")
    raise_for_response(response, "fetching portfolio")

    data = ApiResponse[Portfolio].model_validate_json(response.content).data
    if data is None:
        raise MissingDataError("fetching portfolio")
    return data
