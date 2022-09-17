#!/bin/sh

export GITHUB_TOKEN=$1
export TRACKED_FILE=$2
export GRAI_NAMESPACE=$3
export GRAI_HOST=$4
export GRAI_PORT=$5
export GRAI_AUTH_TOKEN=$6
export PR_NUMBER=$(echo $GITHUB_REF | awk 'BEGIN { FS = "/" } ; { print $3 }')

python3 /src/main.py
