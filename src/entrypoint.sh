#!/bin/sh

export GITHUB_TOKEN=$1
export TRACKED_FILE=$2
export GRAI_NAMESPACE=$3
export GRAI_HOST=$4
export GRAI_PORT=$5

python3 /src/main.py
