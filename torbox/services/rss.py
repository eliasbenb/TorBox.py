from typing import Any, Dict

from requests import Response
from typing_extensions import Optional

from .base import BaseService


class TorBoxRSSError(Exception):
    """Base exception for TorBox RSS errors"""

    pass


class RSSService(BaseService):
    """TorBox RSS service API wrapper"""

    def _handle_response(self, response: Response) -> Dict[str, Any]:
        data = super()._handle_response(response)
        if not response.ok:
            raise TorBoxRSSError(data.get("detail", "Unknown RSS error"))

    def add_feed(
        self,
        url: str,
        regex: Optional[str] = None,
        name: Optional[str] = None,
        interval: Optional[int] = None,
        seed: Optional[int] = None,
        allow_zip: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Add a new RSS feed

        Args:
            url (str): RSS feed URL
            regex (Optional[str]): Regex pattern to filter items
            name (Optional[str]): Custom name for the feed
            interval (Optional[int]): Check interval in minutes
            seed (Optional[int]): Seeding preference (1-3)
            allow_zip (Optional[bool]): Allow zipping downloads

        Returns:
            Dict[str, Any]: The API response
        """
        url_endpoint = f"{self._base_url}/api/rss/addrss"

        data = {
            "url": url,
            "regex": regex,
            "name": name,
            "interval": interval,
            "seed": seed,
            "allow_zip": allow_zip,
        }

        response = self._session.post(url_endpoint, json=data)
        return self._handle_response(response)

    def control_feed(self, rss_id: int, operation: str) -> Dict[str, Any]:
        """Control an RSS feed

        Args:
            rss_id (int): RSS feed ID
            operation (str): Operation to perform

        Returns:
            Dict[str, Any]: The API response
        """
        url = f"{self._base_url}/api/rss/controlrss"

        data = {"rss_id": rss_id, "operation": operation}

        res = self._session.post(url, json=data)
        return self._handle_response(res)

    def modify_feed(
        self,
        rss_id: int,
        regex: Optional[str] = None,
        name: Optional[str] = None,
        interval: Optional[int] = None,
        seed: Optional[int] = None,
        allow_zip: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Modify an existing RSS feed

        Args:
            rss_id (int): RSS feed ID to modify
            regex (Optional[str]): New regex pattern
            name (Optional[str]): New feed name
            interval (Optional[int]): New check interval
            seed (Optional[int]): New seeding preference
            allow_zip (Optional[bool]): New zip setting

        Returns:
            Dict[str, Any]: The API response
        """
        url = f"{self._base_url}/api/rss/modifyrss"

        data = {
            "rss_id": rss_id,
            "regex": regex,
            "name": name,
            "interval": interval,
            "seed": seed,
            "allow_zip": allow_zip,
        }

        res = self._session.post(url, json=data)
        return self._handle_response(res)
