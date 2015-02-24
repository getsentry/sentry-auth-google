from __future__ import absolute_import, print_function

from sentry.plugins import Plugin2

from .provider import GoogleOAuth2Provider


class GoogleAuthPlugin(Plugin2):
    def get_auth_providers(self):
        return [GoogleOAuth2Provider]
