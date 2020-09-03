# Copyright 2020 Cognite AS
FROM sonarsource/sonar-scanner-cli:4

# Github actions must run as root, but sonarqube overrides these
ARG UID=0
ARG GID=0

COPY entrypoint.sh /entrypoint.sh
COPY iap_proxy.py /iap_proxy.py

# Using pip requires a working C build environment
RUN apk add --no-cache \
    py3-requests \
    py3-openssl \
    py3-twisted \
    py3-service_identity \
    curl

ENTRYPOINT ["/entrypoint.sh"]
