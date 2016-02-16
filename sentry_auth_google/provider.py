from __future__ import absolute_import, print_function

from sentry.auth.providers.oauth2 import (
    OAuth2Callback, OAuth2Provider, OAuth2Login
)

from .constants import (
    AUTHORIZE_URL, ACCESS_TOKEN_URL, CLIENT_ID, CLIENT_SECRET, SCOPE
)
from .views import FetchUser, GoogleConfigureView


class GoogleOAuth2Login(OAuth2Login):
    authorize_url = AUTHORIZE_URL
    client_id = CLIENT_ID
    scope = SCOPE

    def __init__(self, domain=None):
        self.domain = domain
        super(GoogleOAuth2Login, self).__init__()

    def get_authorize_params(self, state, redirect_uri):
        params = super(GoogleOAuth2Login, self).get_authorize_params(
            state, redirect_uri
        )
        # TODO(dcramer): ideally we could look at the current resulting state
        # when an existing auth happens, and if they're missing a refresh_token
        # we should re-prompt them a second time with ``approval_prompt=force``
        # params['approval_prompt'] = 'force'
        params['access_type'] = 'offline'
        return params


class GoogleOAuth2Provider(OAuth2Provider):
    name = 'Google'
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET

    def __init__(self, domain=None, **config):
        self.domain = domain
        super(GoogleOAuth2Provider, self).__init__(**config)

    def get_configure_view(self):
        return GoogleConfigureView.as_view()

    def get_auth_pipeline(self):
        return [
            GoogleOAuth2Login(domain=self.domain),
            OAuth2Callback(
                access_token_url=ACCESS_TOKEN_URL,
                client_id=self.client_id,
                client_secret=self.client_secret,
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
