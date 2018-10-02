from . import db
from datetime import datetime


class Utils:

    @staticmethod
    def get_info():
        initTimeDb = db.query('SELECT time FROM EVENT ORDER BY time LIMIT 1').fetchall()
        if len(initTimeDb) == 0:
            initTime = db.query('SELECT time FROM EVENT ORDER BY time LIMIT 1').fetchall()[0][0]
        else:
            initTime = initTimeDb[0][0]
        result = db.query('SELECT * FROM NVR').fetchall()
        refTime = db.query('SELECT * FROM CONF').fetchall()[0][0]
        onDevices = 0
        for device in result:
            if device[4] > device[5]:
                onDevices += 1

        timeDiff = datetime.now() - initTime

        info = {}
        info['onDevices'] = onDevices
        info['allDevices'] = len(result)
        info['initTime'] = initTime.strftime('%Y-%m-%d %H:%M')
        info['runningTimeDays'] = timeDiff.days
        info['runningTimeHours'] = timeDiff.seconds / 3600
        info['refreshTime'] = refTime

        return info
