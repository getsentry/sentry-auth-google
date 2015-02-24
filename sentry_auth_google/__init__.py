from __future__ import absolute_import

from sentry.auth import register

from .provider import GoogleOAuth2Provider

register('google', GoogleOAuth2Provider)
