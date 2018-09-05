from datetime import datetime
from flask import Flask, render_template, json, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import time
import subprocess
import sys

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_DB'] = "NVR"
app.config['MYSQL_DATABASE_HOST'] = "db"

if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    app.config['MYSQL_DATABASE_PORT'] = 32000
    app.config['MYSQL_DATABASE_HOST'] = "127.0.0.1"

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
mysql.init_app(app)

class ReusableForm(Form):
    name = TextField('Pavadinimas:', validators=[validators.required()])
    ipAddress = TextField('IP adresas:', validators=[validators.required()])

@app.route('/ref')
def ref():
    subprocess.call(['python', 'testNVR.py'])
    return redirect(url_for('main'))

@app.route('/delete/<id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM NVR WHERE ID = %s', id)
    conn.commit()

    return redirect(url_for('main'))

@app.route('/nvr/<id>')
def info(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM EVENT WHERE ID = %s', id)
    logsDb = cursor.fetchall()
    logs = []

    for log in logsDb:
        info = []
        info.append(log[1])
        info.append(log[2])
        logs.append(info)

    cursor.execute('SELECT name FROM NVR WHERE id = %s', id)
    name = cursor.fetchall()[0][0]

    info = {
        'name': name,
        'logs': logs
    }
    return render_template('info.html', info=info)

@app.route('/insert', methods=['GET', 'POST'])
def insert():

    form = ReusableForm(request.form)
    if request.method == 'POST':
        name = request.form['name']
        ipAddress = request.form['ipAddress']
        if form.validate():
            conn = mysql.connect()
            cursor = conn.cursor()
            nowDate = time.strftime('%Y-%m-%d')
            nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                'INSERT INTO NVR (ip, name, add_date, off_until_date, on_until_date) VALUES (%s, %s, %s, %s, %s)', \
                (ipAddress, name, nowDate, nowTime, '2010-01-01 01:01:01'))
            conn.commit()
            flash(name + '   irenginys sekmingai pridetas')
        else:
            flash('All the form fields are required. ')
    return render_template('insert.html', form=form)

@app.route("/")
def main():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT time FROM EVENT ORDER BY time LIMIT 1')
    initTimeDb = cursor.fetchall()
    if len(initTimeDb) == 0:
        cursor.execute('SELECT * FROM CONF')
        initTime = cursor.fetchall()[0][0]
    else:
        initTime = initTimeDb[0][0]
    deviceInitTimeStr = '2010-01-01 01:01:01'
    deviceInitTime = datetime.strptime(deviceInitTimeStr, '%Y-%m-%d %H:%M:%S')
    cursor.execute('SELECT * FROM NVR')
    result = cursor.fetchall()
    cursor.execute('SELECT * FROM CONF')
    refTime = cursor.fetchall()[0][0]
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
    timeDiff = datetime.now() - initTime
    info = {}
    info['onDevices'] = onDevices
    info['allDevices'] = len(devices)
    info['initTime'] = initTime.strftime('%Y-%m-%d %H:%M')
    info['runningTimeDays'] = timeDiff.days
    info['runningTimeHours'] = timeDiff.seconds / 3600
    info['refreshTime'] = refTime

    return render_template('index.html', devices=devices, info=info)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.run(host="0.0.0.0", port=8081)
    app.run(host="0.0.0.0", port=8080, debug=True)