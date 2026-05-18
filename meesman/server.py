from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

import httpx
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from meesman.client import create_client
from meesman.endpoints import (
    get_portfolio,
    get_registrations,
    get_transactions,
    get_transactions_paginated,
    get_yields,
    get_yields_chart,
)
from meesman.exceptions import (
    ForbiddenError,
    MeesmanError,
    MissingDataError,
    RequestError,
    UnauthorizedError,
)
from meesman.models import (
    OrderTransaction,
    OrderTransactionsPage,
    Portfolio,
    Registration,
    Yield,
    YieldChart,
)
from meesman.session import SessionState


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    session = SessionState.load()
    if not session.refresh_token:
        raise RuntimeError(
            "No refresh token found in session file. Bootstrap the session before starting the server."
        )
    async with create_client(session) as client:
        app.state.client = client
        yield


app = FastAPI(lifespan=lifespan, title="Meesman API wrapper")


def get_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.client


Client = Annotated[httpx.AsyncClient, Depends(get_client)]


@app.exception_handler(MeesmanError)
async def _meesman_error_handler(request: Request, exc: MeesmanError) -> JSONResponse:
    if isinstance(exc, UnauthorizedError):
        status = 401
    elif isinstance(exc, ForbiddenError):
        status = 403
    elif isinstance(exc, RequestError):
        status = exc.status_code
    elif isinstance(exc, MissingDataError):
        status = 502
    else:
        status = 500
    return JSONResponse({"detail": str(exc)}, status_code=status)


@app.get("/registrations")
async def list_registrations(client: Client) -> list[Registration]:
    return await get_registrations(client)


@app.get("/yields/{registration_id}")
async def list_yields(registration_id: int, client: Client) -> list[Yield]:
    return await get_yields(client, registration_id)


@app.get("/yields/{registration_id}/chart")
async def yields_chart(registration_id: int, client: Client) -> list[YieldChart]:
    return await get_yields_chart(client, registration_id)


@app.get("/portfolios/{registration_id}")
async def portfolio(registration_id: int, client: Client) -> Portfolio:
    return await get_portfolio(client, registration_id)


@app.get("/orders/{registration_id}/transactions")
async def list_transactions(
    registration_id: int,
    client: Client,
) -> list[OrderTransaction]:
    return await get_transactions(client, registration_id)


@app.get("/orders/{registration_id}/transactions/paginated")
async def list_transactions_paginated(
    registration_id: int,
    client: Client,
    page: int = 1,
) -> OrderTransactionsPage:
    return await get_transactions_paginated(
        client, registration_id, page
    )
