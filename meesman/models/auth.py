from datetime import datetime

from meesman.models.base import ApiModel


class RefreshTokenData(ApiModel):
    refresh_token: str
    access_token: str
    expires_at: datetime | None = None
