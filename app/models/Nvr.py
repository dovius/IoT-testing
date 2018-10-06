from . import db
from . import ReusableForm
from datetime import datetime

from flask import Flask, render_template, json, request, redirect, url_for, flash
import time


class Nvr:

    @staticmethod
    def getNvrs():
        deviceInitTimeStr = '2010-01-01 01:01:01'
        deviceInitTime = datetime.strptime(deviceInitTimeStr, '%Y-%m-%d %H:%M:%S')
        result = db.query('SELECT * FROM NVR').fetchall()
        devices = []
        onDevices = 0
        for device in result:
            status = False
            if deviceInitTime == device[4]:
                timeDiff = device[5] - device[4]
            else:
                timeDiff = datetime.now() - device[5]
            if device[4] > device[5]:
                status = True
                onDevices += 1
                timeDiff = datetime.now() - device[4]
            deviceEntity = {
                'id': device[0],
                'ip': device[1],
                'name': str(device[2]).capitalize(),
                'status': status,
                'offTimeDiffDays': timeDiff.days,
                'offTimeDiffHours': timeDiff.seconds / (60 * 60),
                'timeDiff': timeDiff.total_seconds()}
            if timeDiff.days > 500:
                deviceEntity['timeDiff'] = -1
            devices.append(deviceEntity)
        # devices = sorted(devices, key = lambda i: (i['name']))
        devices = sorted(devices, key = lambda i: (i['status'], i['timeDiff']),reverse=True)
        return devices

    @staticmethod
    def getNvr(id):

        deviceInitTimeStr = '2010-01-01 01:01:01'
        deviceInitTime = datetime.strptime(deviceInitTimeStr, '%Y-%m-%d %H:%M:%S')
        result = db.query('SELECT * FROM NVR WHERE id = %s', (id,)).fetchall()
        onDevices = 0
        for device in result:
            status = False
            if deviceInitTime == device[4]:
                timeDiff = device[5] - device[4]
            else:
                timeDiff = datetime.now() - device[5]
            if device[4] > device[5]:
                status = True
                onDevices += 1
                timeDiff = datetime.now() - device[4]
            device = {
                'id': device[0],
                'ip': device[1],
                'name': device[2],
                'status': status,
                'offTimeDiffDays': timeDiff.days,
                'offTimeDiffHours': timeDiff.seconds / (60 * 60),
                'ports': device[6],
                'password': device[7],
                'internal': device[8]
            }
        return device


    @staticmethod
    def insert_nvr():
        form = ReusableForm(request.form)
        if request.method == 'POST':
            name = request.form['name']
            ipAddress = request.form['ipAddress']
            ports = request.form['ports']
            password = request.form['password']
            internal = request.form['internal']
            if form.validate():
                nowDate = time.strftime('%Y-%m-%d')
                nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
                db.query(
                    'INSERT INTO NVR (ip, name, add_date, off_until_date, on_until_date, ports, password, internal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', \
                    (ipAddress, name, nowDate, nowTime, '2010-01-01 01:01:01', ports, password, internal))
                flash(name + '   irenginys sekmingai pridetas')
            else:
                flash('All the form fields are required. ')
        return form

    @staticmethod
    def edit_nvr(id):
        form = ReusableForm(request.form)
        if request.method == 'POST':
            name = request.form['name']
            ipAddress = request.form['ipAddress']
            ports = request.form['ports']
            password = request.form['password']
            internal = request.form['internal']
            if form.validate():
                db.query(
                    'UPDATE NVR SET ip = %s, name = %s, ports = %s, password = %s, internal = %s WHERE id=%s', \
                    (ipAddress, name, ports, password, internal, id))
                flash(name + '   irenginys sekmingai atnaujintas')
            else:
                flash('All the form fields are required. ')
        return form

    @staticmethod
    def delete_nvr(id):
        db.query('DELETE FROM NVR WHERE ID = %s', (id,))
        return
