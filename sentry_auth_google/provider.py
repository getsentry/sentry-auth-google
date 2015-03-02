from __future__ import absolute_import, print_function

from django.conf import settings
from sentry.auth.providers.oauth2 import (
    OAuth2Callback, OAuth2Provider, OAuth2Login
)
from urllib import urlencode

from .constants import (
    AUTHORIZE_URL, ACCESS_TOKEN_URL, CLIENT_ID, CLIENT_SECRET, SCOPE
)
from .views import FetchUser, GoogleConfigureView


class GoogleOAuth2Provider(OAuth2Provider):
    name = 'Google'

    def __init__(self, domain=None, **config):
        self.domain = domain
        super(GoogleOAuth2Provider, self).__init__(**config)

    def get_configure_view(self):
        return GoogleConfigureView.as_view()

    def get_authorize_params(self, state, redirect_uri):
        params = super(GoogleOAuth2Provider, self).get_authorize_params(
            state, redirect_uri
        )
        # without force on approval_prompt we're not guaranteed to receive
        # a refresh_token
        params['approval_prompt'] = 'force'
        params['access_type'] = 'offline'
        if self.domain:
            params['hd'] = self.domain
        return params

    def get_auth_pipeline(self):
        return [
            OAuth2Login(
                authorize_url=AUTHORIZE_URL,
                scope=SCOPE,
                client_id=CLIENT_ID,
            ),
            OAuth2Callback(
                access_token_url=ACCESS_TOKEN_URL,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
            ),
            FetchUser(domain=self.domain),
        ]

    def get_refresh_token_url(self):
        return ACCESS_TOKEN_URL

    def build_config(self, state):
        # TODO(dcramer): we actually want to enforce a domain here. Should that
        # be a view which does that, or should we allow this step to raise
        # validation errors?
        return {
            'domain': state['user']['domain'],
        }

    def build_identity(self, state):
        # data.user => {
        #   "displayName": "David Cramer",
        #   "emails": [{"value": "david@getsentry.com", "type": "account"}],
        #   "domain": "getsentry.com",
        #   "verified": false
        # }
        data = state['data']
        user_data = state['user']
        return {
            'id': user_data['id'],
            # TODO: is there a "correct" email?
            'email': user_data['emails'][0]['value'],
            'name': user_data['displayName'],
            'data': self.get_oauth_data(data),
        }
