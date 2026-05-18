import httpx

from meesman.client import raise_for_response
from meesman.exceptions import MissingDataError
from meesman.models.base import ApiResponse
from meesman.models.registration import Registration


async def get_registrations(client: httpx.AsyncClient) -> list[Registration]:
    response = await client.get("v1/registrations", params={"includeDetails": "true"})
    raise_for_response(response, "fetching registrations")

    data = ApiResponse[list[Registration]].model_validate_json(response.content).data
    if data is None:
        raise MissingDataError("fetching registrations")
    return data
