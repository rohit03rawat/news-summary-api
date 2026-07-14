#!/bin/bash

python -m celery -A news_api worker -l info --pool=solo --concurrency=1 &

python health.py