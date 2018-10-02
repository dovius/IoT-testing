#!/bin/sh
sleep 1m
cron
service cron start
python app/testNVR.py &
python run.py
