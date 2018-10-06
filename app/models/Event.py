from . import db

class Event:

    @staticmethod
    def get_event(id):
        logsDb = db.query('SELECT * FROM EVENT WHERE ID = %s ORDER BY time DESC', (id,)).fetchall()
        logs = []

        for log in logsDb:
            info = []
            info.append(log[1])
            info.append(log[2])
            logs.append(info)

        name = db.query('SELECT name FROM NVR WHERE id = %s', (id,)).fetchall()[0][0]

        info = {
            'name': name,
            'logs': logs
        }
        return info
