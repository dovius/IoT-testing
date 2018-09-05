#!/bin/sh

python app/testNVR.py refresh &
python app/app.py
service cron start
