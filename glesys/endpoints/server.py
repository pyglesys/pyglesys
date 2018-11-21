import os.path

from .base import ApiObject, ApiResource, Endpoint, format_args_get


class Server(ApiResource):
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
    _limits_path = "/server/limits"
    _console_path = "/server/console"
    _costs_path = "/server/costs"

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
        return ServerStatus(**resp.response.server)

    def networkadapters(self):
        path = os.path.join(
            self._networkadapters_path, format_args_get(serverid=self.serverid)
        )
        resp = self.glesys._get(path)
        adapters = [
            NetworkAdapter(**na) for na in resp.response.networkadapters
        ]
        return adapters

    def limits(self):
        # TODO: Test with OpenVZ server
        path = os.path.join(
            self._limits_path, format_args_get(serverid=self.serverid)
        )
        resp = self.glesys._get(path)
        return Limits(**resp.response.limits)

    def console(self):
        path = os.path.join(
            self._console_path, format_args_get(serverid=self.serverid)
        )
        resp = self.glesys._get(path)
        return ConsoleInformation(**resp.response.console)

    def allowed_args(self):
        return self.glesys.server.allowed_args(server_id=self.serverid)

    def costs(self):
        path = os.path.join(
            self._costs_path, format_args_get(serverid=self.serverid)
        )
        resp = self.glesys._get(path)
        return resp.response.costs.todict()


class ServerStatus(ApiObject):
    pass


class NetworkAdapter(ApiObject):
    pass


class Limits(ApiObject):
    pass


class ConsoleInformation(ApiObject):
    pass


class DetailedServer(ApiObject):
    """Represents detailed information about a server."""


class ServerTemplate(ApiObject):
    pass


class ServerEndpoint(Endpoint):
    """Server API endpoint."""

    _ls_path = "/server/list"
    _detail_path = "/server/details"
    _templates_path = "/server/templates"
    _allowed_args_path = "/server/allowedarguments"

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
        return DetailedServer(**resp.response.server, sort_attrs=True)

    def templates(self):
        """Get available operating system templates."""
        resp = self.glesys._get(self._templates_path)
        templates = []
        for group, ts in resp.response.templates.items():
            for t in ts:
                templates.append(ServerTemplate(**t))
        return templates

    def allowed_args(self, server_id=None):
        path = self._allowed_args_path
        if server_id is not None:
            path = os.path.join(
                path, format_args_get(serverid=server_id)
            )
        resp = self.glesys._get(path)
        return resp.response.argumentslist.todict()
