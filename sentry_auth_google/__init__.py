from __future__ import absolute_import

from sentry.auth import register

from .providers.google_oauth2 import GoogleOAuth2Provider

register('google', GoogleOAuth2Provider)
