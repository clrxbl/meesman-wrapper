# meesman-wrapper

An unofficial Python wrapper for the [Meesman Indexbeleggen](https://www.meesman.nl) "public" API. Ships a typed async client and a FastAPI server that exposes the same functionality over HTTP.

Be aware that this is not affiliated with Meesman in any way, and is based on reverse engineering the Meesman Android app as they do not currently provide official API documentation or access. **Use at own risk.**

## Installation

A Docker image is available at [ghcr.io/clrxbl/meesman-wrapper](https://ghcr.io/clrxbl/meesman-wrapper) which you can run with:

```sh
docker run -d \
  -v $(pwd)/data:/app/data \
  -p 127.0.0.1:8000:8000 \
  --name meesman-wrapper \
  ghcr.io/clrxbl/meesman-wrapper
```

## Configuration

There is no login flow in this wrapper as it seems like the API expects a somewhat non-standard OIDC authentication flow, so you are expected to provide valid credentials from a logged-in Meesman client. You can obtain these by inspecting the network traffic of the Meesman Android app using a proxy tool like [HTTP Toolkit](https://httptoolkit.com).

The wrapper expects a `session.json` file which is created at `$cwd/data/session.json` by default. On first run you need to create this file (and directory) manually with a valid `refresh_token` and a `device_id` taken from a logged-in Meesman Android app.

```json
{
  "refresh_token": "<your refresh token from a logged-in Meesman client>",
  "device_id": "<your device ID from a logged-in Meesman client>"
}
```

After setup, the wrapper handles refreshing the refresh token automatically.

## Usage

### Library

```python
import asyncio
from meesman import create_client, SessionState
from meesman.endpoints import get_portfolio, get_registrations

async def main():
    session = SessionState.load()
    async with create_client(session) as client:
        registrations = await get_registrations(client)
        for registration in registrations:
            portfolio = await get_portfolio(client, registration.registration_id)
            print(registration.account_holders, portfolio.total_value)

asyncio.run(main())
```

### HTTP server

```sh
uv run uvicorn meesman.server:app --reload
```

API docs are available at http://127.0.0.1:8000/docs.

## Configuration

| Variable               | Default                          | Purpose                        |
| ---------------------- | -------------------------------- | ------------------------------ |
| `MEESMAN_API_BASE_URL` | `https://public-api.meesman.nl/` | Upstream API base URL.         |
| `MEESMAN_SESSION_FILE` | `session.json`                   | Path to the persisted session. |

## Known issues / caveats

- The session file holds bearer tokens in plaintext. Make sure to secure it properly.
- Enum coverage matches the decompiled Meesman client at the time of writing. Any new upstream enum value will fail Pydantic validation until the relevant `StrEnum` is updated.
