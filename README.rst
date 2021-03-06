py.glesys
=========

``py.glesys`` is a library for accessing the `GleSYS API`_ using Python.


**NOTE**: The project is in its infancy, rely on it at your own peril.

.. _GleSYS API: https://glesys.com/developers

Installing
----------

Install using `pip <https://pip.pypa.io/en/stable/>`_::

    $ pip install pyglesys


Example Usage
-------------

.. code-block:: python

    import glesys

    gs = glesys.Glesys('account_number', 'api_key')
    servers = gs.server.list()
    print(servers)

.. code-block:: console

    $ python app.py
    [Server({'serverid': 'wps1234567', 'hostname': 'example.com', 'datacenter': 'Falkenberg', 'platform': 'VMware'})]


Disclaimer
----------

This project is not associated with GleSYS AB in any way. I'm just a private
person doing this for fun.
