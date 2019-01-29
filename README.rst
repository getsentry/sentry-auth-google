Google Auth for Sentry
======================

An SSO provider for Sentry which enables Google Apps authentication.

Install
-------

For Sentry >= 8.23.0:
::

    $ pip install sentry-auth-google
    
For Sentry <= 8.22.0 (`See Issue <https://github.com/getsentry/sentry-auth-google/issues/21>`_):
::

    $ pip install https://github.com/getsentry/sentry-auth-google/archive/52020f577f587595fea55f5d05520f1473deaad1.zip

Setup
-----

Start by `creating a project in the Google Developers Console <https://console.developers.google.com>`_.

Then, create an OAuth Client ID/Secret pair via `Project Credentials <https://console.developers.google.com/apis/credentials>`_.

In the **Authorized redirect URIs** add the SSO endpoint for your installation::

    https://sentry.example.com/auth/sso/

Finally, obtain the API keys and plug them into your ``sentry.conf.py``:

.. code-block:: python

    GOOGLE_CLIENT_ID = ""

    GOOGLE_CLIENT_SECRET = ""

