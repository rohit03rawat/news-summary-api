#!/bin/bash

python -m celery -A news_api worker -l info &

python health.py