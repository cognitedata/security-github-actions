#!/usr/bin/env python3

from sys import stderr
import os
import json
import requests
from urllib.parse import quote as urlquote

from google.oauth2.service_account import IDTokenCredentials
from google.oauth2 import id_token
from google.auth.transport.requests import Request

from twisted.internet import reactor, ssl
from twisted.web import proxy, server
from twisted.protocols.tls import TLSMemoryBIOFactory
from twisted.logger import globalLogBeginner, textFileLogObserver


globalLogBeginner.beginLoggingTo([textFileLogObserver(stderr)])

def get_oidc_token(request, client_id, service_account):
    sa_info = json.loads(service_account)
    credentials = IDTokenCredentials.from_service_account_info(
        sa_info, target_audience=client_id
    )
    credentials.refresh(request)
    return credentials.token

def exchange_google_id_token_for_gcip_id_token(api_key, google_open_id_connect_token):
  SIGN_IN_WITH_IDP_API = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp'    
  url = SIGN_IN_WITH_IDP_API + '?key=' + api_key
  data={'requestUri': 'http://localhost',
        'returnSecureToken': True,
        'postBody':'id_token=' + google_open_id_connect_token + '&providerId=google.com'}
  resp = requests.post(url, data)
  res = resp.json()
  return res['idToken']


class IAPReverseProxyResource(proxy.ReverseProxyResource):
    def proxyClientFactoryClass(self, *args, **kwargs):
        return TLSMemoryBIOFactory(
            ssl.optionsForClientTLS(self.host),
            True,
            super().proxyClientFactoryClass(*args, **kwargs),
        )

    def __init__(self, id_token, custom_auth_header, target_uri, target_port, path=b""):
        super().__init__(target_uri, target_port, path)
        self.id_token = id_token
        self.custom_auth_header = custom_auth_header

    def render(self, request):
        if self.custom_auth_header and request.requestHeaders.hasHeader(b"authorization"):
            request.requestHeaders.setRawHeaders(
                self.custom_auth_header,
                request.requestHeaders.getRawHeaders(b"authorization", []),
            )

        request.requestHeaders.setRawHeaders(b"authorization", ['Bearer {}'.format(self.id_token)])

        return super().render(request)

    def getChild(self, path, request):
        return IAPReverseProxyResource(
            self.id_token,
            self.custom_auth_header,
            self.host,
            self.port,
            self.path + b"/" + urlquote(path, safe=b"").encode("utf-8"),
        )

custom_auth_header = os.environ.get("IAP_CUSTOM_AUTH_HEADER")
target_host = os.environ["IAP_TARGET_HOST"]
target_port = (
    int(os.environ.get("IAP_TARGET_PORT")) if os.environ.get("TARGET_PORT") else 443
)
client_id = os.environ["IAP_CLIENT_ID"]
sa_data = os.environ["IAP_SA"]
api_key = os.environ["API_KEY"]

open_id_connect_token = get_oidc_token(Request(), client_id, sa_data)
id_token = exchange_google_id_token_for_gcip_id_token(api_key, open_id_connect_token)

site = server.Site(
    IAPReverseProxyResource(id_token, custom_auth_header, target_host, target_port)
)

reactor.listenTCP(9000, site, interface="127.0.0.1")
reactor.run()