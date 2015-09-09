from __future__ import absolute_import, print_function

from django.conf import settings


AUTHORIZE_URL = 'https://accounts.google.com/o/oauth2/auth'

ACCESS_TOKEN_URL = 'https://www.googleapis.com/oauth2/v3/token'

CLIENT_ID = getattr(settings, 'GOOGLE_CLIENT_ID', None)

CLIENT_SECRET = getattr(settings, 'GOOGLE_CLIENT_SECRET', None)

ERR_INVALID_DOMAIN = 'The domain for your Google account is not allowed to authenticate with this provider.'

SCOPE = 'email'

# requires Google+ API enabled
USER_DETAILS_ENDPOINT = 'https://www.googleapis.com/plus/v1/people/me'
