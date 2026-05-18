from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, field_validator

from meesman.config import settings


class SessionState(BaseModel):
    refresh_token: str = ""
    access_token: str = ""
    access_token_expiry: datetime | None = None
    device_id: str = ""

    @field_validator("access_token_expiry", mode="before")
    @classmethod
    def _blank_to_none(cls, v: Any) -> Any:
        return None if v == "" else v

    @classmethod
    def load(cls, path: Path | None = None) -> "SessionState":
        path = path or settings.session_file
        return cls.model_validate_json(path.read_text())

    def save(self, path: Path | None = None) -> None:
        path = path or settings.session_file
        path.write_text(self.model_dump_json(indent=2))
