from flask import Flask, render_template, json, request, redirect, url_for, flash

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.secret_key = "super secret key"

    from errors.handlers import errors
    from controllers.nvr import nvr
    app.register_blueprint(errors)
    app.register_blueprint(nvr)

    return app

