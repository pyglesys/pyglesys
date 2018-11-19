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

    _networkadapters_path = "/server/networkadapters"
    _status_path = "/server/status"

    def details(self):
        """Get details of this server.

        Returns
        -------
        DetailedServer
            Detailed information about this server.
        """
        return self.glesys.server.details(self.serverid)

    def status(self, include=None):
        """Get server status.

        Args
        ----
        include : list of str
            A list of what information to include. Allowed values are
            ``state``, ``cpu``, ``memory``, ``disk`` or ``uptime``. The
            default is to include all information.

        Returns
        -------
        ServerStatus
            Status information for the server.
        """
        if include is not None:
            include = ",".join(include)
        args = {"serverid": self.serverid, "statustype": include}
        resp = self.glesys._post(self._status_path, args)
        return ServerStatus(self.glesys, **resp.response.server)

    def networkadapters(self):
        path = os.path.join(
            self._networkadapters_path, format_args_get(serverid=self.serverid)
        )
        resp = self.glesys._get(path)
        adapters = [
            NetworkAdapter(self.glesys, **na) for na in resp.response.networkadapters
        ]
        return adapters


class ServerStatus(ApiObject):
    pass


class NetworkAdapter(ApiObject):
    pass


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
