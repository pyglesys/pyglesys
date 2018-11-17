import os.path

from .base import ApiObject, Endpoint, format_args_get


class Server(ApiObject):
    """Represents a server resource as returned by the API.

    Attributes
    ----------
    serverid : str
        GleSYS assigned server ID.
    hostname : str
        The hostname of the server.
    datacenter : str
        The data center of the server.
    platform : str
        The virtualisation platform (``VMware`` of ``OpenVZ``).
    """

    def details(self):
        """Get details of this server.

        Returns
        -------
        DetailedServer
            Detailed information about this server.
        """
        return self.glesys.server.details(self.serverid)


class DetailedServer(ApiObject):
    """Represents detailed information about a server."""


class ServerEndpoint(Endpoint):
    """Server API endpoint."""

    _ls_path = "/server/list"
    _detail_path = "/server/details"

    def list(self):
        """List servers on the account.

        Returns
        -------
        ``list`` of :class:`Server`
            A list of the servers for the account.
        """
        resp = self.glesys._get(self._ls_path)
        servers = []
        for s in resp.response.servers:
            servers.append(Server(self.glesys, **s))
        return servers

    def details(self, server_id):
        """Get details of a server.

        Returns
        -------
        DetailedServer
            Detailed information about the server.
        """
        path = os.path.join(self._detail_path, format_args_get(serverid=server_id))
        resp = self.glesys._get(path)
        return DetailedServer(
            self.glesys, **resp.response.server, sort_attrs=True
        )
