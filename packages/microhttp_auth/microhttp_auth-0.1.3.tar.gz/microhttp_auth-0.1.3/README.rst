microhttp-auth
==============

.. image:: https://img.shields.io/pypi/pyversions/microhttp-auth.svg
    :target: https://pypi.python.org/pypi/microhttp-auth

.. image:: https://travis-ci.org/meyt/microhttp-auth.svg?branch=master
    :target: https://travis-ci.org/meyt/microhttp-auth

.. image:: https://coveralls.io/repos/github/meyt/microhttp-auth/badge.svg?branch=master
    :target: https://coveralls.io/github/meyt/microhttp-auth?branch=master

Role based JWT stateless/ful authentication module for
`microhttp <https://github.com/meyt/microhttp>`_.



Install
-------


.. code-block:: bash

    pip install microhttp-auth

Note: Need to setup ``redis`` database, if using stateful authenticator.


Configuration
-------------

.. code-block:: yaml

    auth:
      jwt_secret_key: <SECRET_KEY>
      jwt_algorithm: # Algorithm supported by pyjwt
      redis:  # Redis configuration [optional]
        host:
        port:
