python-requirejs
================

Run RequireJS (r.js) from Python without requiring Node or Rhino.
Leverages `PyMiniRacer <https://github.com/sqreen/PyMiniRacer>`__ plus a
minimal `JS
environment <https://github.com/wq/python-requirejs/blob/master/requirejs/env.js>`__
to make r.js think it's running in node.

|Latest PyPI Release| |Release Notes| |License| |GitHub Stars| |GitHub
Forks| |GitHub Issues|

|Travis Build Status| |Python Support|

Usage
-----

``python-requirejs`` is available via PyPI:

.. code:: bash

    pip install requirejs

API
~~~

.. code:: python

    import requirejs

    requirejs.optimize(
        appDir=".",
        baseUrl="js/",
        modules=[{
            "name": "main",
        }]
        dir="../build",
    )

Hopefully, all of the `available build options for
r.js <http://requirejs.org/docs/optimization.html#options>`__ will Just
Work. If you find any discrepancies, please `open a
ticket <https://github.com/wq/python-requirejs/issues>`__ to let us
know.

This library is meant to be a drop-in replacement for
``node r.js -o app.build.json``, and is tested by comparing its output
with that command. However, since the optimize API is being called as a
function, you may need to set the working directory explicitly to avoid
any unexpected differences in how relative paths are computed:

.. code:: python

    import requirejs
    import json

    with open('app/app.build.json') as f:
        config = json.load(f)

    requirejs.optimize(
        config,
        working_directory="app/"  # Unique to python-requirejs
    )

.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/requirejs.svg
   :target: https://pypi.org/project/requirejs/
.. |Release Notes| image:: https://img.shields.io/github/release/wq/python-requirejs.svg
   :target: https://github.com/wq/python-requirejs/releases
.. |License| image:: https://img.shields.io/pypi/l/requirejs.svg
   :target: https://github.com/wq/python-requirejs/blob/master/LICENSE
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/python-requirejs.svg
   :target: https://github.com/wq/python-requirejs/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/python-requirejs.svg
   :target: https://github.com/wq/python-requirejs/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/python-requirejs.svg
   :target: https://github.com/wq/python-requirejs/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/python-requirejs/master.svg
   :target: https://travis-ci.org/wq/python-requirejs
.. |Python Support| image:: https://img.shields.io/pypi/pyversions/requirejs.svg
   :target: https://pypi.org/project/requirejs/
