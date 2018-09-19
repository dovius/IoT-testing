#!/bin/sh
sleep 1m
cron
service cron start
python app/testNVR.py refresh &
python run.py
