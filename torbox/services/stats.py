from typing import Any, Dict

from requests import Response

from .base import BaseService


class StatsError(Exception):
    """Base exception for TorBox stats errors"""

    pass


class StatsService(BaseService):
    """TorBox stats service API wrapper"""

    def _handle_response(self, response: Response, **kwargs) -> Dict[str, Any]:
        data = super()._handle_response(response, **kwargs)
        if not response.ok:
            raise StatsError("Unknown stats error")

        return data

    def stats(self) -> Dict[str, Any]:
        """Get TorBox stats

        Returns:
            Dict[str, Any]: API response
        """

        url = f"{self._base_url}/api/stats"
        self._throttle_request()
        res = self._session.get(url)
        return self._handle_response(res)
