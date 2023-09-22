README
======

dtool CLI plugin for querying dependency graph from dtool lookup server.

Installation
------------

To install the dtool-lookup-client-dependency-graph-plugin

.. code-block:: bash

    pip install dtool-lookup-client-dependency-graph-plugin

This plugin depends on having a `dtool-lookup-server
<https://github.com/jic-dtool/dtool-lookup-server>`_ with
`dtool-lookup-server-dependency-graph-plugin` installed to talk to.

Looking up dpendency graph of dataset by UUID
---------------------------

To lookup dependency graph starting at dataset UUID::

    dtool graph UUID

Specify dependency key to process
---------------------------------

To build dependency graph using specific keys for UUIDs::

    dtool graph UUID --dependency-keys derived_from

To access specific page of results::

    dtool graph UUID --page-number 3 --page-size 40

To show pagination inormation before listing results, use::

    dtool --debug graph UUID

You will see info like

    INFO - Pagination information: {'total': 1, 'total_pages': 1, 'first_page': 1, 'last_page': 1, 'page': 1}
