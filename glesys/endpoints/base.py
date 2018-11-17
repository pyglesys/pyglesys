import collections
import operator


def format_args_get(**kwargs):
    args = ""
    for k, v in kwargs.items():
        args += "{}/{}".format(k, v)
    return args


class ApiObject(collections.MutableMapping):
    """Represents an object returned from the API.

    ``ApiObject`` instances behave basically like :class:`dict` with the
    addition of the handy dot notation for accessing attributes (i.e.
    keys) as well as (optionally) sorting attributes alphabetically for
    output.

    Keyword Args
    ------------
    glesys : Glesys
        A GleSYS instance.
    sort_attrs : bool
        Wether or not attributes should be sorted in output.
    """

    def __init__(self, glesys, sort_attrs=False, **kwargs):
        self.glesys = glesys
        self._sort_attrs = sort_attrs
        self._dict = dict(**kwargs)

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __delitem__(self, key, value):
        self._dict[key] = value

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            msg = "'{}' object has no attribute '{}'"
            raise AttributeError(msg.format(self.__class__.__name__, attr))

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        attrs = self.items()
        if self._sort_attrs:
            attrs = sorted(attrs, key=operator.itemgetter(0))
        return "{}({})".format(self.__class__.__name__, dict(attrs))


class Endpoint(object):
    """Base class for all endpoints."""

    def __init__(self, glesys):
        self.glesys = glesys
