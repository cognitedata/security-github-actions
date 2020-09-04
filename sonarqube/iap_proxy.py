#!/usr/bin/env python3

from sys import stderr
import os
import json
from urllib.parse import quote as urlquote

from msrestazure.azure_active_directory import AADTokenCredentials
import adal

from twisted.internet import reactor, ssl
from twisted.web import proxy, server
from twisted.protocols.tls import TLSMemoryBIOFactory
from twisted.logger import globalLogBeginner, textFileLogObserver


globalLogBeginner.beginLoggingTo([textFileLogObserver(stderr)])

# Authenticate using service principal w/ key.
def get_iap_access_token(aad_tenant, client_id, client_secret):
    
    authority_host_uri = 'https://login.microsoftonline.com'
    authority_uri = authority_host_uri + '/' + aad_tenant
    resource_uri = 'https://management.core.windows.net/'

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    mgmt_token = context.acquire_token_with_client_credentials(resource_uri, client_id, client_secret)
    accessToken = mgmt_token.get("accessToken")

    return accessToken


class IAPReverseProxyResource(proxy.ReverseProxyResource):
    def proxyClientFactoryClass(self, *args, **kwargs):
        return TLSMemoryBIOFactory(
            ssl.optionsForClientTLS(self.host),
            True,
            super().proxyClientFactoryClass(*args, **kwargs),
        )

    def __init__(self, accessToken, custom_auth_header, target_uri, target_port, path=b""):
        super().__init__(target_uri, target_port, path)
        self.accessToken = accessToken
        self.custom_auth_header = custom_auth_header

    def render(self, request):
        if self.custom_auth_header and request.requestHeaders.hasHeader(b"authorization"):
            request.requestHeaders.setRawHeaders(
                self.custom_auth_header,
                request.requestHeaders.getRawHeaders(b"authorization", []),
            )

        request.requestHeaders.setRawHeaders(b"authorization", [accessToken])        

        return super().render(request)

    def getChild(self, path, request):
        return IAPReverseProxyResource(
            self.accessToken,
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
aad_tenant = os.environ["AAD_TENANT"]
client_id = os.environ["IAP_CLIENT_ID"]
client_secret = os.environ["IAP_CLIENT_SECRET"]

accessToken = get_iap_access_token(aad_tenant, client_id, client_secret)

site = server.Site(
    IAPReverseProxyResource(accessToken, custom_auth_header, target_host, target_port)
)
reactor.listenTCP(9000, site, interface="127.0.0.1")
reactor.run()
