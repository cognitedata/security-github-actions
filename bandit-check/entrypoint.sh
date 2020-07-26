#!/bin/sh -l
# Copyright 2020 Cognite AS

echo "Scanning project: $1"
bandit --version
REPORT=$(bandit -r $1)
REPORT="${REPORT//'%'/'%25'}"
REPORT="${REPORT//$'\n'/'%0A'}"
REPORT="${REPORT//$'\r'/'%0D'}"
echo "::set-output name=report::$REPORT"
