from collections import Mapping


class Box(Mapping):
    """An immutable dict-like object with dot notation.

    Example
    -------
    Simple example:

        >>> from glesys.box import Box
        >>> box = Box({'hello': 'world'})
        >>> box
        Box({'hello': 'world'})
        >>> box.hello
        'world'

    It supports nested dicts:

        >>> from glesys.box import Box
        >>> box = Box({'hello': {'recursive': {'world': 42}}})
        >>> box
        Box({'hello': {'recursive': {'world': 42}}})
        >>> box.hello.recursive.world
        42
    """

    __slots__ = ["__dict"]

    def __init__(self, *args, **kwargs):
        self.__dict = dict(*args, **kwargs)

    def __getitem__(self, key):
        return self.__dict[key]

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)

    def __repr__(self):
        return "Box({})".format(self.__dict)

    def __getattr__(self, item):
        value = self[item]
        if isinstance(value, dict):
            value = Box(value)
        if isinstance(value, list):
            value = [Box(v) for v in value]
        if isinstance(value, tuple):
            value = tuple(Box(v) for v in value)
        return value

    def to_dict(self):
        """Return a copy of the box as a regular dict.

        Returns
        -------
        dict:
            A copy of the Box as a regular dict.
        """
        return dict(self.__dict)
