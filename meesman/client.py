import asyncio
from uuid import uuid4

import httpx

from meesman.config import settings
from meesman.exceptions import ForbiddenError, RequestError, UnauthorizedError
from meesman.session import SessionState


class MeesmanAuth(httpx.Auth):
    def __init__(self, session: SessionState):
        self.session = session
        self._lock = asyncio.Lock()

    async def async_auth_flow(self, request: httpx.Request):
        # Lazy import to avoid a circular dependency: refresh_access_token
        # calls create_client, which constructs MeesmanAuth.
        from meesman.endpoints.auth import refresh_access_token

        request.headers["Authorization"] = f"Bearer {self.session.access_token}"
        response = yield request
        if response.status_code != 401:
            return

        async with self._lock:
            async with create_client(self.session, authenticated=False) as client:
                await refresh_access_token(client, self.session)

        request.headers["Authorization"] = f"Bearer {self.session.access_token}"
        yield request


def create_client(session: SessionState, authenticated: bool = True) -> httpx.AsyncClient:
    # The Meesman API seems to require a unique client request ID for most requests
    async def inject_request_id(request: httpx.Request) -> None:
        request.headers["client-request-id"] = str(uuid4())

    # The app also passes along the device ID with every request
    headers = {"meesman-device-id": session.device_id}
    auth: httpx.Auth | None = None

    if authenticated:
        if not session.access_token:
            raise ValueError("Access token is required for authenticated client.")
        auth = MeesmanAuth(session)

    return httpx.AsyncClient(
        base_url=settings.api_base_url,
        headers=headers,
        auth=auth,
        event_hooks={"request": [inject_request_id]},
    )


def raise_for_response(response: httpx.Response, action: str) -> None:
    if response.status_code == 401:
        raise UnauthorizedError(f"Received unauthorized response from Meesman while {action}.")
    if response.status_code == 403:
        raise ForbiddenError(f"Received forbidden response from Meesman while {action}.")
    if not response.is_success:
        raise RequestError(action, response.status_code)
