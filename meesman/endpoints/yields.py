import httpx

from meesman.client import raise_for_response
from meesman.exceptions import MissingDataError
from meesman.models.base import ApiResponse
from meesman.models.yields import Yield, YieldChart


async def get_yields(client: httpx.AsyncClient, registration_id: int) -> list[Yield]:
    response = await client.get(f"v1/yields/{registration_id}")
    raise_for_response(response, "fetching yields")

    data = ApiResponse[list[Yield]].model_validate_json(response.content).data
    if data is None:
        raise MissingDataError("fetching yields")
    return data


async def get_yields_chart(client: httpx.AsyncClient, registration_id: int) -> list[YieldChart]:
    response = await client.get(f"v1/yields/{registration_id}/chart")
    raise_for_response(response, "fetching yield chart")

    data = ApiResponse[list[YieldChart]].model_validate_json(response.content).data
    if data is None:
        raise MissingDataError("fetching yield chart")
    return data
