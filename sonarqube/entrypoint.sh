#!/bin/bash -le
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

PR_ARGS=()
if [[ "$GITHUB_REF" == refs/pull/*/merge ]] && \
       [ -n "PR_SOURCE_BRANCH" ] && [ -n "PR_TARGET_BRANCH" ]; then
    PR_ID="${GITHUB_REF##refs/pull/}"
    PR_ID="${PR_ID%%/merge}"

    PR_ARGS=(
        "-Dsonar.pullrequest.branch=$PR_SOURCE_BRANCH"
        "-Dsonar.pullrequest.key=$PR_ID"
        "-Dsonar.pullrequest.base=$PR_TARGET_BRANCH"
    )
fi

"$SONAR_SCANNER_HOME"/bin/sonar-scanner \
    -Dsonar.projectKey="$REPO_NAME" \
    -Dsonar.projectName="$REPO_NAME" \
    -Dsonar.sources="$PROJECT_PATH" \
    -Dsonar.host.url="http://localhost:9000" \
    -Dsonar.login="$SONARQUBE_TOKEN" \
    "${PR_ARGS[@]}"
