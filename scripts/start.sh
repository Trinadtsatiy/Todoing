#! /bin/bash

source env/env.sh

yoyo-migrate apply --batch

cd backend/ || exit 1

gunicorn -c gunicorn.conf.py