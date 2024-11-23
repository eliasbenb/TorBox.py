from .services import (
    BaseService,
    IntegrationsServices,
    RSSService,
    StatsService,
    TorrentsService,
    UsenetService,
    UserService,
    WebDLService,
)


class TorBox(BaseService):
    """TorBox API Client"""

    def __init__(self, api_key: str, base_url: str = "https://api.torbox.app/v1"):
        super().__init__(api_key, base_url)

        service_args = (api_key, base_url, self._session)

        self.integrations = IntegrationsServices(*service_args)
        self.rss = RSSService(*service_args)
        self.stats = StatsService(*service_args)
        self.torrents = TorrentsService(*service_args)
        self.usenet = UsenetService(*service_args)
        self.user = UserService(*service_args)
        self.webdl = WebDLService(*service_args)
