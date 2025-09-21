#!/usr/bin/env bash

pkill gunicorn
find . -name "*.pyc" -delete
rm -rf exams/__pycache__ exam_app/__pycache__
gunicorn --bind 0.0.0.0:8000 exam_app.wsgi --daemon
