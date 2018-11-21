from .base import ApiObject, Endpoint
from ..exceptions import AuthenticationException, GlesysException


class User(ApiObject):
    pass


class UserEndpoint(Endpoint):
    _detail_path = "/user/details/"
    _login_path = "/user/login/"

    def details(self):
        """Get details of the currently logged in user."""
        resp = self.glesys._get(self._detail_path)
        return User(**resp.response.user, sort_attrs=True)

    def login(self, username, password):
        """Authenticate using a username and password.

        Note
        ----
            Users will probably want to call :meth:`Glesys.login
            <glesys.Glesys.login>` instead of accessing this method
            directly.

        This method is used to retrieve a temporary API key for the
        user. If it's called when the Glesys instance is already
        authenticated, a :class:`ValueError` is raised. This is a
        precaution since logging in with a username and password would
        otherwise overwrite the API key and sidestep limitations that
        were put on it.

        Warning
        -------
        This method should only be used for local testing, when
        deploying a project using pyglesys, pass an account number and
        API key to the :class:`Glesys constructor <glesys.Glesys>` instead.

        Args
        ----
        username : str
            The username of the user to authenticate.
        password : str
            The password of the user to authenticate.

        Returns
        -------
        account : str
            Account number to use in later requests.
        api_key : str
            The API key to use in later requests.

        Raises
        ------
        ~glesys.exceptions.AuthenticationException
            If the username or password is wrong.
        ValueError
            If the instance is already authenticated.
        """
        if self.glesys.has_auth_info:
            raise ValueError("Authentication information already present.")

        data = {"username": username, "password": password}
        try:
            res = self.glesys._post(self._login_path, data, bypass_authcheck=True)
        except GlesysException as e:
            raise AuthenticationException(e)

        account = res.response.login.accounts[0].account
        api_key = res.response.login.apikey

        return (account, api_key)
