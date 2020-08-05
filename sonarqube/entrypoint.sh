#!/bin/sh -le
# Copyright 2020 Cognite AS

echo "Scanning project $GITHUB_REPOSITORY/$PROJECT_PATH"

export IAP_CUSTOM_AUTH_HEADER="X-Sq-Authorization"
python3 /iap_proxy.py &
proxy_pid="$!"

function atexit() {
    kill "$proxy_pid"
    echo "Waiting for proxy ($proxy_pid) to terminate"
    wait "$proxy_pid"
}
trap atexit SIGINT SIGTERM EXIT

echo -n "Waiting for proxy"
until curl -s "http://localhost:9000" -o /dev/null; do
    echo -n "."
    sleep 1
done
echo ""

REPO_NAME="${GITHUB_REPOSITORY##*/}"

"$SONAR_SCANNER_HOME"/bin/sonar-scanner \
    -Dsonar.projectKey="$REPO_NAME" \
    -Dsonar.projectName="$REPO_NAME" \
    -Dsonar.sources="$PROJECT_PATH" \
    -Dsonar.host.url="http://localhost:9000" \
    -Dsonar.login="$SONARQUBE_TOKEN"
