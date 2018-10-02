import MySQLdb


class DB:
    conn = None

    def connect(self):
        self.conn = MySQLdb.connect(host="db", user='root', db="NVR", port=3306)
        self.conn.autocommit(True)

    def query(self, sql, args=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, args)
            return cursor
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor


db = DB()