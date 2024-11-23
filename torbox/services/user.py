from typing import Any, Dict

from requests import Response

from .base import BaseService


class UserError(Exception):
    """Base exception for TorBox user errors"""

    pass


class UserService(BaseService):
    """TorBox user service API wrapper"""

    def _handle_response(self, response: Response, **kwargs) -> Dict[str, Any]:
        data = super()._handle_response(response, **kwargs)
        if not response.ok:
            raise UserError("Unknown user error")

        return data
