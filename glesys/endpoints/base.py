import operator

import sys
if sys.version_info[0] == 2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin


class ApiObject(object):
    """Base class for objects returned from the API."""

    def __init__(self, attrs, sort_attrs=False):
        self.attrs = attrs
        self._sort_attrs = sort_attrs

    def __getattr__(self, attr):
        try:
            return self.attrs[attr]
        except KeyError:
            msg = "'{}' not found in {}"
            raise AttributeError(msg.format(attr, self.__class__.__name__))

    def __repr__(self):
        attrs = self.attrs.items()
        if self._sort_attrs:
            attrs = sorted(attrs, key=operator.itemgetter(0))
        return "{}({})".format(self.__class__.__name__, dict(attrs))


class Endpoint(object):
    """Base class for all endpoints."""
    def __init__(self, glesys):
        self.glesys = glesys

    def _get(self, path, **kwargs):
        url = self._prepare_get(path, **kwargs)
        return self.glesys.s.get(url).json()

    def _prepare_url(self, path):
        return urljoin(self.glesys.API_BASE, path)

    def _prepare_get(self, path, **kwargs):
        url = self._prepare_url(path)
        args = ""
        for k, v in kwargs.items():
            args += "{}/{}".format(k, v)
        return urljoin(url, args)
