#!/bin/bash

set -e

if [ "$1" = 'crawl' ]; then
    export PYTHONPATH="${PYTHONPATH}:/opt/" && \
        cd /opt/crawler/ && \
	python ./crawl.py $@;
    exit 0
fi

if [ "$1" = 'parse' ]; then
	echo "$@"
    export PYTHONPATH="${PYTHONPATH}:/opt/" && \
        cd /opt/parser/ && \
	python ./parser.py $@;
    exit 0
fi
