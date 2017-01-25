from datetime import datetime
from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
import config

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = config.dbUser
app.config['MYSQL_DATABASE_PASSWORD'] = config.dbPassword
app.config['MYSQL_DATABASE_DB'] = config.dbTable
app.config['MYSQL_DATABASE_HOST'] = config.dbHost
mysql.init_app(app)


@app.route("/")
def main():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT time FROM EVENT ORDER BY time LIMIT 1')
    initTimeDb = cursor.fetchall()
    initTime = initTimeDb[0][0]
    cursor.execute('SELECT * FROM NVR')
    result = cursor.fetchall()
    devices = []
    onDevices = 0
    for device in result:
        status = False
        timeDiff = device[5] - device[4]
        if device[4] > device[5]:
            status = True
            onDevices += 1
            timeDiff = datetime.now() - device[4]
        deviceEntity = {
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
    info['initTime'] = initTime.strftime('%Y-%d-%m %H:%M')
    info['runningTimeDays'] = timeDiff.days
    info['runningTimeHours'] = timeDiff.seconds / 3600

    return render_template('index.html', devices=devices, info=info)


if __name__ == "__main__":
    app.run(host='localhost', port='8080')
