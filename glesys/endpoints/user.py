from .base import ApiObject, Endpoint


class User(ApiObject):
    pass


class UserEndpoint(Endpoint):
    _detail_path = "/user/details/"

    def details(self):
        """Get details of a server."""
        resp = self._get(self._detail_path)
        return User(resp['response']['user'], sort_attrs=True)
