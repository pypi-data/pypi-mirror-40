import json

import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from django_allauth_steemconnect.providers.steemconnect.provider import SteemConnectProvider


class SteemConnectOAuth2Adapter(OAuth2Adapter):
    provider_id = SteemConnectProvider.id
    access_token_url = 'https://steemconnect.com/api/oauth2/token'
    authorize_url = 'https://steemconnect.com/oauth2/authorize'
    revoke_url = 'https://steemconnect.com/api/oauth2/token/revoke'
    profile_url = 'https://steemconnect.com/api/me'
    scope_delimiter = ','

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url, headers={
            'Authorization': token.token
        })
        extra_data = json.loads(resp.content)
        return self.get_provider().sociallogin_from_response(
            request,
            extra_data
        )


oauth2_login = OAuth2LoginView.adapter_view(SteemConnectOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SteemConnectOAuth2Adapter)
