#!/bin/bash

celery -A news_api worker -l info &

gunicorn news_api.wsgi:application --bind 0.0.0.0:$PORT