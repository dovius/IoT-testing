from flask import Blueprint, render_template, redirect, url_for, request, session,  make_response
from . import LoginForn, login_required
import subprocess

from app.models.Nvr import Nvr
from app.models.Event import Event
from app.services.utils import Utils

nvr = Blueprint('nvr', __name__)


@nvr.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForn
    if request.method == 'POST':
        password = request.form.get('password')
        remember = request.form.get('remember')

        if password == 'almamater':
            if remember != 'on':
                session['login'] = 'admin'
                return redirect(url_for('nvr.get_nvr'))
            else:
                resp = make_response(redirect(url_for('nvr.get_nvr')))
                resp.set_cookie('login', 'admin')
                return resp
        else:
            return render_template('login.html', form=form)


    return render_template('login.html', form=form)

@nvr.route('/', methods=['GET'])
@login_required
def get_nvr():
    devices = Nvr.getNvrs()
    info = Utils.get_info()
    return render_template('index.html', devices=devices, info=info)

@nvr.route('/insert', methods=['GET'])
@login_required
def insert():
    form = Nvr.insert_nvr()
    return render_template('insert.html', form=form)

@nvr.route('/insert', methods=['POST'])
@login_required
def insertPost():
    form = Nvr.insert_nvr()
    return redirect(url_for('nvr.get_nvr'))

@nvr.route('/event/<id>', methods=['GET', 'POST'])
@login_required
def get_event(id):
    eventInfo = Event.get_event(id)
    nvrInfo = Nvr.getNvr(id)
    form = Nvr.edit_nvr(id)
    if request.method == 'POST':
        return redirect(url_for('nvr.get_nvr'))
    return render_template('info.html', info=eventInfo, nvrInfo=nvrInfo, form=form)


@nvr.route('/delete/<id>')
@login_required
def delete(id):
    Nvr.delete_nvr(id)
    return redirect(url_for('nvr.get_nvr'))

@nvr.route('/ref')
@login_required
def ref():
    subprocess.call(['python', 'testNVR.py'])
    return redirect(url_for('main'))

@nvr.route('/logout')
@login_required
def logout():
    resp = make_response(redirect(url_for('nvr.get_nvr')))
    resp.set_cookie('login', '')
    session['login'] = ''
    return resp



