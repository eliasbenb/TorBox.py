import importlib.metadata
import time
from typing import Any, Dict

import requests
from typing_extensions import Optional

_VERSION = importlib.metadata.version("torbox")


class TorBoxError(Exception):
    """Base exception for TorBox errors"""

    pass


class TorBoxAuthenticationError(TorBoxError):
    """Exception for authentication errors"""

    pass


class TorBoxRateLimitError(TorBoxError):
    """Exception for rate limit errors"""

    pass


class BaseService:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        session: requests.Session = requests.Session(),
    ):
        self._session = session
        self._base_url = base_url
        self._api_key = api_key
        self._last_default_request_time = 0
        self._last_create_request_time = 0
        self._default_request_rate = 0.2
        self._create_request_rate = 6

        self._session.headers.update(
            {
                "Authorization": f"Bearer {self._api_key}",
                "User-Agent": f"TorBox.py/{_VERSION}",
            }
        )

    def _throttle_request(self, is_create: Optional[bool] = False):
        """Ensure minimum time interval between requests

        Args:
            is_create (Optional[bool]): Whether the request is a create request. Defaults to False.
        """
        current_time = time.time()

        if is_create:
            time_since_last_request = current_time - self._last_create_request_time
            time_to_wait = self._create_request_rate - time_since_last_request
        else:
            time_since_last_request = current_time - self._last_default_request_time
            time_to_wait = self._default_request_rate - time_since_last_request

        if time_to_wait > 0:
            time.sleep(time_to_wait)

        self._last_request_time = time.time()

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors

        Args:
            response (requests.Response): The API response

        Raises:
            AuthenticationError: When authentication fails
            RateLimitError: When rate limit is exceeded
            TorBoxError: When an unknown error occurs

        Returns:
            Dict[str, Any]: The API response
        """
        try:
            data = response.json()
        except ValueError:
            raise TorBoxError("Invalid JSON response from API")

        if not response.ok:
            if response.status_code == 403:
                raise TorBoxAuthenticationError(
                    data.get("detail", "Authentication failed")
                )
            elif response.status_code == 429:
                raise TorBoxRateLimitError(data.get("detail", "Rate limit exceeded"))
            elif response.status_code == 500:
                raise TorBoxError(data.get("detail", "Internal server error"))

        return data
