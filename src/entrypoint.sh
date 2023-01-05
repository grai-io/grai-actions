#!/bin/sh

export GITHUB_TOKEN=$1
export TRACKED_FILE=$2
export GRAI_NAMESPACE=$3
export GRAI_HOST=$4
export GRAI_PORT=$5
export GRAI_API_KEY=$6
export GRAI_WORKSPACE=$7
export GRAI_FRONTEND_HOST=$8
export PR_NUMBER=$(echo $GITHUB_REF | awk 'BEGIN { FS = "/" } ; { print $3 }')

python3 /src/main.py
