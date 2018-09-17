from flask import request, redirect, url_for, session
from functools import wraps
from wtforms import Form, TextField, validators


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        loginCookie = request.cookies.get('login')
        loginSession = session.get('login')
        print loginSession
        print loginCookie
        if loginCookie == 'admin' or loginSession == 'admin':
            return f(*args, **kwargs)
        return redirect(url_for('nvr.login'))
    return wrap

class LoginForn(Form):
    password = TextField('Password:', validators=[validators.required()])