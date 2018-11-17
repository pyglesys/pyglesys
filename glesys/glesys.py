import sys

import requests

from .exceptions import AuthenticationException, GlesysException
from . import endpoints
from ._box import Box

if sys.version_info[0] == 2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin


class Glesys(object):
    """Main class for interacting with the GleSYS API.

    If ``account`` and ``api_key`` are omitted, the :meth:`login` method
    has to be called before trying to access any API resources.

    Args
    ----
    account : str, optional
        The GleSYS account to use when accessing the API.
    api_key : str, optional
        The API key to use when accessing the API.

    Note
    ----
    Due to the way authentication information is handled, providing
    wrong credentials in ``account`` or ``api_key`` won't be noticed
    until the first endpoint is called, at which point an
    :class:`~glesys.exceptions.AuthenticationException` is raised.

    Providing the wrong credentials to :meth:`login` will however raise
    an ``AuthenticationException`` immediately.
    """

    #: Base URL for the API
    API_BASE = "https://api.glesys.com"

    #: ServerEndpoint: Server endpoint.
    server = None
    #: UserEndpoint: User endpoint.
    user = None
    #: AccountEndpoint: Account endpoint.
    account = None

    def __init__(self, account=None, api_key=None):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        if account and api_key:
            self._setup_auth(account, api_key)
        elif account or api_key:
            msg = "Both or neither `account' and `api_key' must be specified"
            raise ValueError(msg)
        self.server = endpoints.ServerEndpoint(self)
        self.user = endpoints.UserEndpoint(self)
        self.account = endpoints.AccountEndpoint(self)

    @property
    def has_auth_info(self):
        return self.session.auth is not None

    def login(self, username, password):
        """Authenticate using a username and password

        For details, see :meth:`UserEndpoint.login <endpoints.UserEndpoint.login>`
        """
        account, api_key = self.user.login(username, password)
        self._setup_auth(account, api_key)

    def _get(self, path):
        if not self.has_auth_info:
            raise AuthenticationException("Not authenticated to perform API calls.")

        url = urljoin(self.API_BASE, path)
        response = self.session.get(url)
        data = Box(response.json())

        # Check if something went wrong.
        if response.status_code != 200:
            raise GlesysException(data.response.status.text)

        return data

    def _post(self, path, data, bypass_authcheck=False):
        if not bypass_authcheck and not self.has_auth_info:
            raise AuthenticationException("Not authenticated to perform API calls.")

        url = urljoin(self.API_BASE, path)
        response = self.session.post(url, json=data)
        resp_data = Box(response.json())

        if response.status_code != 200:
            raise GlesysException(resp_data.response.status.text)

        return resp_data

    def _setup_auth(self, account, api_key):
        # Create authenticated Session that later requests are made via
        self.session.auth = (account, api_key)
