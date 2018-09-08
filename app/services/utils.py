from . import cursor
from datetime import datetime


class Utils:

    @staticmethod
    def get_info():
        cursor.execute('SELECT time FROM EVENT ORDER BY time LIMIT 1')
        initTimeDb = cursor.fetchall()
        if len(initTimeDb) == 0:
            cursor.execute('SELECT * FROM CONF')
            initTime = cursor.fetchall()[0][0]
        else:
            initTime = initTimeDb[0][0]
        cursor.execute('SELECT * FROM NVR')
        result = cursor.fetchall()
        cursor.execute('SELECT * FROM CONF')
        refTime = cursor.fetchall()[0][0]
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
