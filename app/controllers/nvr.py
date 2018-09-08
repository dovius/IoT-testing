from flask import Blueprint, render_template, redirect, url_for
import subprocess

from app.models.Nvr import Nvr
from app.models.Event import Event
from app.services.utils import Utils

nvr = Blueprint('nvr', __name__)


@nvr.route('/', methods=['GET'])
def get_nvr():
    devices = Nvr.get_nvr()
    info = Utils.get_info()
    return render_template('index.html', devices=devices, info=info)

@nvr.route('/insert', methods=['GET', 'POST'])
def insert():
    form = Nvr.insert_nvr()
    return render_template('insert.html', form=form)

@nvr.route('/event/<id>', methods=['GET'])
def get_event(id):
    info = Event.get_event(id)
    return render_template('info.html', info=info)

@nvr.route('/delete/<id>')
def delete(id):
    Nvr.delete_nvr(id)
    return redirect(url_for('nvr.get_nvr'))

@nvr.route('/ref')
def ref():
    subprocess.call(['python', 'testNVR.py'])
    return redirect(url_for('main'))

