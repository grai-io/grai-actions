#!/bin/bash

export PR_NUMBER=$(echo $GITHUB_REF | awk 'BEGIN { FS = "/" } ; { print $3 }')

grai-actions
