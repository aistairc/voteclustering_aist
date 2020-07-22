#!/bin/sh
python3 manage.py migrate
yarn build
python3 manage.py compilemessages
python3 manage.py collectstatic --noinput
