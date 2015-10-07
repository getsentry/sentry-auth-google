Google Auth for Sentry
======================

An SSO provider for Sentry which enables Google Apps authentication.

Install
-------

::

    $ pip install https://github.com/getsentry/sentry-auth-google/archive/master.zip

Setup
-----

Start by `creating a project in the Google Developers Console <https://console.developers.google.com>`_.

In the **Authorized redirect URIs** add the SSO endpoint for your installation::

    https://sentry.example.com/auth/sso/

You will also need to enable the **Google+ API**.

Finally, obtain the API keys and plug them into your ``sentry.conf.py``:

.. code-block:: python

    GOOGLE_CLIENT_ID = ""

    GOOGLE_CLIENT_SECRET = ""

