import httpx

from meesman.client import raise_for_response
from meesman.exceptions import MissingDataError
from meesman.models.auth import RefreshTokenData
from meesman.models.base import ApiResponse
from meesman.session import SessionState


async def refresh_access_token(client: httpx.AsyncClient, session: SessionState) -> str:
    params = {"refreshToken": session.refresh_token, "deviceId": session.device_id}
    response = await client.get("v1/user/refreshAccessToken", params=params)
    raise_for_response(response, "refreshing access token")

    data = ApiResponse[RefreshTokenData].model_validate_json(response.content).data
    if data is None:
        raise MissingDataError("refreshing access token")

    session.refresh_token = data.refresh_token
    session.access_token = data.access_token
    session.access_token_expiry = data.expires_at
    session.save()
    return session.access_token
