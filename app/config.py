import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SERVER_NAME = 'bevardis:8081'
    # SESSION_COOKIE_DOMAIN = 'bevardis:8081'

