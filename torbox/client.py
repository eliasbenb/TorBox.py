from .services.base import BaseService
from .services import TorrentsService, UsenetService, WebDLService


class TorBox(BaseService):
    """TorBox API Client"""

    def __init__(self, api_key: str, base_url: str = "https://api.torbox.app/v1"):
        super().__init__(api_key, base_url)

        self.torrents = TorrentsService(self._api_key, self._base_url, self._session)
        self.usenet = UsenetService(self._api_key, self._base_url, self._session)
        self.webdl = WebDLService(self._api_key, self._base_url, self._session)
