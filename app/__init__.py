from flask import Flask, render_template, json, request, redirect, url_for, flash
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.config.from_pyfile('config.py')
    app.secret_key = "super secret key"

    from errors.handlers import errors
    from controllers.nvr import nvr
    app.register_blueprint(errors)
    app.register_blueprint(nvr)
    # app.register_blueprint(login_manager)

    return app
