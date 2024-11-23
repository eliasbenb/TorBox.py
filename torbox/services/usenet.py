from enum import Enum
from typing import Any, Dict, List

from requests import Response
from typing_extensions import Optional

from .base import BaseService


class TorBoxUsenetError(Exception):
    """Base exception for TorBox usenet errors"""

    pass


class UsenetControlOperation(str, Enum):
    DELETE = "delete"
    PAUSE = "pause"
    RESUME = "resume"


class UsenetService(BaseService):
    """TorBox usenet service API wrapper"""

    def _handle_response(self, response: Response, **kwargs) -> Dict[str, Any]:
        data = super()._handle_response(response, **kwargs)
        if not response.ok:
            raise TorBoxUsenetError("Unknown usenet error")

        return data

    def create(
        self,
        link: Optional[str] = None,
        nzb_file: Optional[str] = None,
        name: Optional[str] = None,
        password: Optional[str] = None,
        post_processing: int = -1,
    ) -> Dict[str, Any]:
        """Create a new usenet download

        Args:
            link (Optional[str]): Link to NZB file
            nzb_file (Optional[str]): Local NZB file path
            name (Optional[str]): Custom name for the download
            password (Optional[str]): Password for extraction
            post_processing (int): Post processing option (-1 to 3)

        Returns:
            Dict[str, Any]: The API response
        """
        url = f"{self._base_url}/api/usenet/createusenetdownload"

        if not link and not nzb_file:
            raise ValueError("Must provide either link or NZB file")
        if link and nzb_file:
            raise ValueError("Cannot provide both link and NZB file")

        data = {
            "link": link,
            "file": ("nzb.nzb", open(nzb_file, "rb")) if nzb_file else None,
            "name": name,
            "password": password,
            "post_processing": post_processing,
        }

        self._throttle_request(is_create=True)
        response = self._session.post(url, data=data)
        return self._handle_response(response)

    def control(
        self, usenet_id: int, operation: UsenetControlOperation
    ) -> Dict[str, Any]:
        """Control a usenet download

        Args:
            usenet_id (int): Usenet download ID
            operation (UsenetControlOperation): Operation to perform

        Returns:
            Dict[str, Any]: The API response
        """
        url = f"{self._base_url}/api/usenet/controlusenetdownload"

        data = {"usenet_id": usenet_id, "operation": operation}

        self._throttle_request()
        res = self._session.post(url, json=data)
        return self._handle_response(res)

    def download(
        self,
        usenet_id: int,
        file_id: Optional[int] = None,
        zip_link: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """Request a download link for a usenet download

        Args:
            usenet_id (int): The usenet download ID
            file_id (Optional[int]): Specific file ID to download
            zip_link (Optional[bool]): Request a zip download link

        Returns:
            Dict[str, Any]: The API response containing download URL
        """
        url = f"{self._base_url}/api/usenet/requestdl"

        params = {"usenet_id": usenet_id, "zip_link": zip_link}
        if file_id:
            params["file_id"] = file_id

        self._throttle_request()
        res = self._session.get(url, params=params)
        return self._handle_response(res)

    def list(
        self,
        usenet_id: Optional[int] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
        bypass_cache: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """List usenet downloads

        Args:
            usenet_id (Optional[int]): Filter by specific download ID
            offset (Optional[int]): Pagination offset
            limit (Optional[int]): Items per page
            bypass_cache (Optional[bool]): Bypass cached response

        Returns:
            Dict[str, Any]: List of usenet downloads
        """
        url = f"{self._base_url}/api/usenet/mylist"

        params = {"bypass_cache": bypass_cache, "offset": offset, "limit": limit}

        if usenet_id:
            params["id"] = usenet_id

        self._throttle_request()
        res = self._session.get(url, params=params)
        return self._handle_response(res)

    def is_cached(
        self,
        usenet_hashes: List[str] | str,
        list_files: Optional[bool] = False,
        bypass_cache: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """Check if usenet downloads are cached

        Args:
            usenet_hashes (List[str] | str): Hash(es) to check
            list_files (Optional[bool]): Include file listings
            bypass_cache (Optional[bool]): Bypass cached response

        Returns:
            Dict[str, Any]: Cache status for requested hashes
        """
        url = f"{self._base_url}/api/usenet/checkcached"

        params = {
            "hash": usenet_hashes
            if isinstance(usenet_hashes, str)
            else ",".join(usenet_hashes),
            "list_files": list_files,
            "bypass_cache": bypass_cache,
            "format": "list",
        }

        self._throttle_request()
        res = self._session.get(url, params=params)
        return self._handle_response(res)
