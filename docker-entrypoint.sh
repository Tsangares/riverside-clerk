#!/bin/bash

set -e

if [ "$1" = 'crawl' ]; then
    export PYTHONPATH="${PYTHONPATH}:/opt/" && \
        cd /opt/crawler/ && \
	python ./crawl.py $@;
    exit 0
fi
