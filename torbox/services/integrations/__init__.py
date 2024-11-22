from ..base import BaseService
import requests


class IntegrationsServices(BaseService):
    def __init__(
        self,
        api_key: str,
        base_url: str,
        session: requests.Session = requests.Session(),
    ):
        super().__init__(api_key, base_url, session)
