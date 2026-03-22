#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: start.sh [PROCESS_TYPE]"
    exit 1
fi

PROCESS_TYPE=$1

if [ "$PROCESS_TYPE" = "server" ]; then
    if [ "$DEBUG" = "true" ]; then
        gunicorn \
          --reload \
          --bind 0.0.0.0:8000 \
          --workers 2 \
          pocket_flow.wsgi:application
    else
        gunicorn \
          --bind 0.0.0.0:8000 \
          --workers 2 \
          pocket_flow.wsgi:application
    fi
fi