from .base import ApiObject, Endpoint


class Account(ApiObject):
    pass


class AccountEndpoint(Endpoint):
    """Account API endpoint."""

    _info_path = "/account/info"

    def info(self):
        """Get information on currently logged in account."""
        resp = self.glesys._get(self._info_path)
        return Account(**resp.response.accountinfo)
