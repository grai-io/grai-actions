#!/bin/sh

export GITHUB_TOKEN=$1
export TRACKED_FILE=$2

python3 src/main.py
