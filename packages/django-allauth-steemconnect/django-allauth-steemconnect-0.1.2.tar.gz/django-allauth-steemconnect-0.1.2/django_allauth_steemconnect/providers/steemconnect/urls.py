from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import SteemConnectProvider

urlpatterns = default_urlpatterns(SteemConnectProvider)
