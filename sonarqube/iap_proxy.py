#!/usr/bin/env python3

from sys import stderr
import os
import json
from urllib.parse import quote as urlquote

from google.oauth2.service_account import IDTokenCredentials
from google.auth.transport.requests import Request

from twisted.internet import reactor, ssl
from twisted.web import proxy, server
from twisted.protocols.tls import TLSMemoryBIOFactory
from twisted.logger import globalLogBeginner, textFileLogObserver


globalLogBeginner.beginLoggingTo([textFileLogObserver(stderr)])


def get_iap_creds(client_id, service_account):
    sa_info = json.loads(service_account)
    return IDTokenCredentials.from_service_account_info(
        sa_info, target_audience=client_id
    )


class IAPReverseProxyResource(proxy.ReverseProxyResource):
    def proxyClientFactoryClass(self, *args, **kwargs):
        return TLSMemoryBIOFactory(
            ssl.optionsForClientTLS(self.host),
            True,
            super().proxyClientFactoryClass(*args, **kwargs),
        )

    def __init__(self, creds, custom_auth_header, target_uri, target_port, path=b""):
        super().__init__(target_uri, target_port, path)
        self.creds = creds
        self.custom_auth_header = custom_auth_header

    def render(self, request):
        if self.custom_auth_header and request.requestHeaders.hasHeader(b"authorization"):
            request.requestHeaders.setRawHeaders(
                self.custom_auth_header,
                request.requestHeaders.getRawHeaders(b"authorization", []),
            )

        extraHeaders = {}
        self.creds.before_request(Request(), None, None, extraHeaders)

        for h, v in extraHeaders.items():
            request.requestHeaders.setRawHeaders(h.encode("ascii"), [v.encode("ascii")])

        return super().render(request)

    def getChild(self, path, request):
        return IAPReverseProxyResource(
            self.creds,
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

creds = get_iap_creds(client_id, sa_data)

site = server.Site(
    IAPReverseProxyResource(creds, custom_auth_header, target_host, target_port)
)
reactor.listenTCP(9000, site, interface="127.0.0.1")
reactor.run()
