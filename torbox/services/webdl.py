from enum import Enum
from typing import Any, Dict

from requests import Response
from typing_extensions import Optional

from .base import BaseService


class TorBoxWebDLError(Exception):
    """Base exception for TorBox web download errors"""

    pass


class WebDLControlOperation(str, Enum):
    DELETE = "delete"


class WebDLService(BaseService):
    """TorBox web download service API wrapper"""

    def _handle_response(self, response: Response) -> Dict[str, Any]:
        data = super()._handle_response(response)
        if not response.ok:
            raise TorBoxWebDLError(data.get("detail", "Unknown web download error"))

    def create(
        self,
        link: str,
        password: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new web download

        Args:
            link (str): URL to download
            password (Optional[str]): Password if required
            name (Optional[str]): Custom name for the download

        Returns:
            Dict[str, Any]: The API response
        """
        url = f"{self._base_url}/api/webdl/createwebdownload"

        data = {"link": link, "password": password, "name": name}

        self._throttle_request(is_create=True)
        response = self._session.post(url, data=data)
        return self._handle_response(response)

    def control(
        self, webdl_id: int, operation: WebDLControlOperation
    ) -> Dict[str, Any]:
        """Control a web download

        Args:
            webdl_id (int): Web download ID
            operation (WebDLControlOperation): Operation to perform

        Returns:
            Dict[str, Any]: The API response
        """
        url = f"{self._base_url}/api/webdl/controlwebdownload"

        data = {"webdl_id": webdl_id, "operation": operation}

        self._throttle_request()
        res = self._session.post(url, json=data)
        return self._handle_response(res)

    def download(
        self,
        webdl_id: int,
        file_id: Optional[int] = None,
        zip_link: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """Request a download link for a web download

        Args:
            webdl_id (int): The web download ID
            file_id (Optional[int]): Specific file ID to download
            zip_link (Optional[bool]): Request a zip download link

        Returns:
            Dict[str, Any]: The API response containing download URL
        """
        url = f"{self._base_url}/api/webdl/requestdl"

        params = {"webdl_id": webdl_id, "zip_link": zip_link}
        if file_id:
            params["file_id"] = file_id

        res = self._session.get(url, params=params)
        return self._handle_response(res)

    def list(
        self,
        webdl_id: Optional[int] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
        bypass_cache: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """List web downloads

        Args:
            webdl_id (Optional[int]): Filter by specific download ID
            offset (Optional[int]): Pagination offset
            limit (Optional[int]): Items per page
            bypass_cache (Optional[bool]): Bypass cached response

        Returns:
            Dict[str, Any]: List of web downloads
        """
        url = f"{self._base_url}/api/webdl/mylist"

        params = {"bypass_cache": bypass_cache, "offset": offset, "limit": limit}

        if webdl_id:
            params["id"] = webdl_id

        res = self._session.get(url, params=params)
        return self._handle_response(res)

    def is_cached(
        self,
        webdl_hashes: list[str] | str,
        list_files: Optional[bool] = False,
        bypass_cache: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """Check if web downloads are cached

        Args:
            webdl_hashes (list[str] | str): Hash(es) to check
            list_files (Optional[bool]): Include file listings
            bypass_cache (Optional[bool]): Bypass cached response

        Returns:
            Dict[str, Any]: Cache status for requested hashes
        """
        url = f"{self._base_url}/api/webdl/checkcached"

        params = {
            "hash": webdl_hashes
            if isinstance(webdl_hashes, str)
            else ",".join(webdl_hashes),
            "list_files": list_files,
            "bypass_cache": bypass_cache,
            "format": "list",
        }

        res = self._session.get(url, params=params)
        return self._handle_response(res)
