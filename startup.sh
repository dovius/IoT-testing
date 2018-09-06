#!/bin/sh

cron
service cron start
python app/testNVR.py refresh &
python app/app.py
