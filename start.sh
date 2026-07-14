#!/bin/bash

gunicorn news_api.wsgi:application --bind 0.0.0.0:$PORT