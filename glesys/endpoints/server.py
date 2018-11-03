from .base import ApiObject, Endpoint


class Server(ApiObject):
    pass


class ServerEndpoint(Endpoint):
    """Server API endpoint."""

    _ls_path = "/server/list"
    _detail_path = "/server/details/"

    def list(self):
        """List available servers."""
        resp = self._get(self._ls_path)
        servers = []
        for s in resp['response']['servers']:
            servers.append(Server(s))
        return servers

    def details(self, server_id):
        """Get details of a server."""
        resp = self._get(self._detail_path, serverid=server_id)
        server = Server(resp['response']['server'], sort_attrs=True)
        return server
