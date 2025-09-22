#!/bin/bash

# Run a root of exam-app
git pull origin main
pip install -r requirements.txt
python3 manage.py collectstatic --noinput
python3 manage.py migrate
systemctl restart gunicorn
systemctl restart nginx
