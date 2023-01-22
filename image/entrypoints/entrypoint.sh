#!/bin/bash

export PR_NUMBER=$(echo $GITHUB_REF | awk 'BEGIN { FS = "/" } ; { print $3 }')


python /grai-actions/src/grai_actions/main.py
#echo $(ls /grai-actions/src)
