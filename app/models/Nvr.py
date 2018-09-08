from . import cursor, db
from . import ReusableForm
from datetime import datetime

from flask import Flask, render_template, json, request, redirect, url_for, flash
import time

class Nvr:

    @staticmethod
    def get_nvr():
        cursor.execute('SELECT time FROM EVENT ORDER BY time LIMIT 1')
        deviceInitTimeStr = '2010-01-01 01:01:01'
        deviceInitTime = datetime.strptime(deviceInitTimeStr, '%Y-%m-%d %H:%M:%S')
        cursor.execute('SELECT * FROM NVR')
        result = cursor.fetchall()
        cursor.execute('SELECT * FROM CONF')
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
                'name': device[2],
                'status': status,
                'offTimeDiffDays': timeDiff.days,
                'offTimeDiffHours': timeDiff.seconds / (60 * 60)}
            devices.append(deviceEntity)
        return devices

    @staticmethod
    def insert_nvr():
        form = ReusableForm(request.form)
        if request.method == 'POST':
            name = request.form['name']
            ipAddress = request.form['ipAddress']
            if form.validate():
                nowDate = time.strftime('%Y-%m-%d')
                nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    'INSERT INTO NVR (ip, name, add_date, off_until_date, on_until_date) VALUES (%s, %s, %s, %s, %s)', \
                    (ipAddress, name, nowDate, nowTime, '2010-01-01 01:01:01'))
                db.commit()
                flash(name + '   irenginys sekmingai pridetas')
            else:
                flash('All the form fields are required. ')
        return form

    @staticmethod
    def delete_nvr(id):
        cursor.execute('DELETE FROM NVR WHERE ID = %s', (id,))
        db.commit()
        return
