from . import cursor, db

class Event:

    @staticmethod
    def get_event(id):
        cursor.execute('SELECT * FROM EVENT WHERE ID = %s', (id,))
        logsDb = cursor.fetchall()
        logs = []

        for log in logsDb:
            info = []
            info.append(log[1])
            info.append(log[2])
            logs.append(info)

        cursor.execute('SELECT name FROM NVR WHERE id = %s', (id,))
        name = cursor.fetchall()[0][0]

        info = {
            'name': name,
            'logs': logs
        }
        return info
