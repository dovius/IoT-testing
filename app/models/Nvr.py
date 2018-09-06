from . import cursor

class Nvr:

    def getNvr(self):
        cursor.execute('SELECT * FROM NVR')
        return cursor.fetchall()