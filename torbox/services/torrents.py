import os
from enum import Enum, IntEnum
from typing import Any, Dict, List

from requests import Response
from typing_extensions import Optional

from .base import BaseService


class TorBoxTorrentsError(Exception):
    """Base exception for TorBox torrent errors"""

    pass


class TorrentsSeedSettings(IntEnum):
    DEFAULT = 1
    ENABLE = 2
    DISABLE = 3


class TorrentsControlOperation(str, Enum):
    DELETE = "delete"
    PAUSE = "pause"
    RESUME = "resume"
    REANNOUNCE = "reannounce"


class TorrentsExportType(str, Enum):
    MAGNET = "magnet"
    FILE = "file"


class TorrentsService(BaseService):
    """TorBox torrent service API wrapper"""

    def _handle_response(self, response: Response) -> Dict[str, Any]:
        data = super()._handle_response(response)
        if not response.ok:
            raise TorBoxTorrentsError(data.get("detail", "Unknown torrents error"))

        return data

    def create(
        self,
        magnet: Optional[str] = None,
        torrent_file: Optional[str] = None,
        seed: Optional[TorrentsSeedSettings] = TorrentsSeedSettings.DEFAULT,
        allow_zip: bool = False,
        name: Optional[str] = None,
        as_queued: bool = False,
    ) -> Dict[str, Any]:
        """Create a new torrent download

        Args:
            magnet (Optional[str]): The torrent's magnet link (if any). Defaults to None.
            torrent_file (Optional[str]): The torrent file (if any). Defaults to None.
            seed (Optional[int]): Use default seed settings = 1, enable seeding = 2, disable seeding = 3. Defaults to 1.
            allow_zip (Optional[bool]): Allow torrent to be zipped. Defaults to False.
            name (Optional[str]): The name TorBox should assign the torrent (if any). Defaults to None.
            as_queued (Optional[bool]): Whether the torrent should be instantly queued. Defaults to False.

        Returns:
            Dict[str, Any]: The API response

        Raises:
            AuthenticationError: When authentication fails
            RateLimitError: When rate limit is exceeded
            TorBoxError: When an unknown error occurs
            ValueError: When invalid arguments are provided
            FileNotFoundError: When a torrent file is passed and it does not exist
        """
        url = f"{self._base_url}/api/torrents/createtorrent"

        if not magnet and not torrent_file:
            raise ValueError("Must provide either magnet or torrent file")
        if magnet and torrent_file:
            raise ValueError("Cannot provide both magnet and torrent file")
        if torrent_file and not os.path.isfile(torrent_file):
            raise FileNotFoundError("Torrent file does not exist")

        data = {
            "magnet": magnet,
            "seed": seed,
            "allow_zip": allow_zip,
            "as_queued": as_queued,
            "name": name,
        }
        files = {}
        if torrent_file:
            torrent_file = os.path.abspath(torrent_file)
            files["file"] = ("torrent.torrent", open(torrent_file, "rb"))

        self._throttle_request(is_create=True)
        response = self._session.post(url, data=data, files=files)
        return self._handle_response(response)

    def control(
        self, torrent_id: int, operation: TorrentsControlOperation
    ) -> Dict[str, Any]:
        """Control a torrent (delete, pause, resume, reannounce)

        Args:
            torrent_id (int): Torrent UID
            operation (str): Operation to perform (delete, pause, resume, reannounce)

        Returns:
            Dict[str, Any]: The API response

        Raises:
            AuthenticationError: When authentication fails
            RateLimitError: When rate limit is exceeded
            TorBoxError: When an unknown error occurs
        """
        url = f"{self._base_url}/api/torrents/controltorrent"

        data = {"torrent_id": torrent_id, "operation": operation}

        self._throttle_request()
        res = self._session.post(url, json=data)
        return self._handle_response(res)

    def download(
        self,
        torrent_id: int,
        file_id: Optional[int] = None,
        zip_link: Optional[bool] = False,
        torrent_file: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """Request a download link for a torrent

        Args:
            torrent_id (int): The torrent's ID
            file_id (Optional[int]): The specific file ID to download
            zip_link (Optional[bool]): Request a zip download link
            torrent_file (Optional[bool]): Request the .torrent file

        Returns:
            Dict[str, Any]: The API response containing the download URL
        """
        url = f"{self._base_url}/api/torrents/requestdl"

        params = {
            "torrent_id": torrent_id,
            "zip_link": zip_link,
            "torrent_file": torrent_file,
        }
        if file_id:
            params["file_id"] = file_id

        self._throttle_request()
        res = self._session.get(url, params=params)
        return self._handle_response(res)

    def list(
        self,
        torrent_id: Optional[int] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 1000,
        bypass_cache: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """List torrents in the user's list

        Args:
            torrent_id (Optional[int]): Torrent ID to filter by. Defaults to None.
            offset (Optional[int]): Pagination offset. Defaults to 0.
            limit (Optional[int]): Number of items per page. Defaults to 1000.
            bypass_cache (Optional[bool]): Bypass response cache. Defaults to False.

        Returns:
            Dict[str, Any]: List of torrents
        """
        url = f"{self._base_url}/api/torrents/mylist"

        params = {"bypass_cache": bypass_cache, "offset": offset, "limit": limit}

        if torrent_id:
            params["id"] = torrent_id

        self._throttle_request()
        res = self._session.get(url, params=params)
        return self._handle_response(res)

    def list_queued(self) -> Dict[str, Any]:
        """Get list of queued torrents for the user

        Returns:
            Dict[str, Any]: List of queued torrents
        """
        url = f"{self._base_url}/api/torrents/getqueued"

        res = self._session.get(url)
        return self._handle_response(res)

    def is_cached(
        self,
        torrent_hashes: List[str] | str,
        list_files: Optional[bool] = False,
        bypass_cache: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """Check if the requested torrents are cached

        Args:
            torrent_hashes (List[str] | str): List of torrent hashe(s) to check.
            list_files (Optional[bool]): List files in each torrent. Defaults to False.
            bypass_cache (Optional[bool]): Bypass cached response data.

        Returns:
            Dict[str, Any]: API response
        """

        url = f"{self._base_url}/api/torrents/checkcached"

        params = {
            "hash": torrent_hashes.join(
                "," if isinstance(torrent_hashes, list) else torrent_hashes
            ),
            "list_files": list_files,
            "bypass_cache": bypass_cache,
            "format": "list",
        }

        hashes = (
            torrent_hashes if isinstance(torrent_hashes, list) else [torrent_hashes]
        )
        if len(hashes) == 0:
            raise ValueError("At least one torrent hash must be provided")
        for hash in hashes:
            if not hash.isalnum() or len(hash) < 40:
                raise ValueError(f"Invalid torrent hash: {hash}")

        self._throttle_request()
        res = self._session.get(url, params=params)
        return self._handle_response(res)

    def search(self, query: str) -> Dict[str, Any]:
        """Search for torrents using the scraper

        Args:
            query (str): Search query string

        Returns:
            Dict[str, Any]: Search results containing torrent information
        """
        url = f"{self._base_url}/api/torrents/search"

        params = {"query": query}

        res = self._session.get(url, params=params)
        return self._handle_response(res)

    def export(
        self, torrent_id: int, export_type: TorrentsExportType
    ) -> Dict[str, Any]:
        """Export torrent data as magnet link or torrent file

        Args:
            torrent_id (int): ID of the torrent to export
            export_type (TorrentsExportType): Type of export. Either "magnet" or "file"

        Returns:
            Dict[str, Any]: For magnet links, returns data containing the magnet URI
                        For torrent files, returns the file download response
        """
        url = f"{self._base_url}/api/torrents/exportdata"

        params = {"torrent_id": torrent_id, "type": export_type}

        self._throttle_request()
        res = self._session.get(url, params=params)
        return self._handle_response(res)

    def info(self, torrent_hash: str, timeout: Optional[int] = 10) -> Dict[str, Any]:
        """Get detailed information about a torrent from the network

        Args:
            torrent_hash (str): Hash of the torrent to look up
            timeout (Optional[int]): Search timeout in seconds (default: 10)

        Returns:
            Dict[str, Any]: Torrent metadata including name, size, files etc.
        """
        url = f"{self._base_url}/api/torrents/torrentinfo"

        params = {"hash": torrent_hash, "timeout": timeout}

        self._throttle_request()
        res = self._session.get(url, params=params)
        return self._handle_response(res)
