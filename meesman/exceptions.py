class MeesmanError(Exception):
    """Base exception for the Meesman client."""


class UnauthorizedError(MeesmanError):
    """Raised when the API returns 401 Unauthorized."""


class ForbiddenError(MeesmanError):
    """Raised when the API returns 403 Forbidden."""


class RequestError(MeesmanError):
    """Raised when an API request fails with a non-success status."""

    def __init__(self, action: str, status_code: int):
        super().__init__(f"Error while {action}: HTTP {status_code}")
        self.action = action
        self.status_code = status_code


class MissingDataError(MeesmanError):
    """Raised when a successful response is missing its expected data payload."""

    def __init__(self, action: str):
        super().__init__(f"No data returned while {action}")
        self.action = action
