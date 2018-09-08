#!/bin/sh

cron
service cron start
python app/testNVR.py refresh &
python run.py
