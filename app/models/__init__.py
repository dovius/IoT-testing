import MySQLdb
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

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


class ReusableForm(Form):
    name = TextField('Pavadinimas:', validators=[validators.required()])
    ipAddress = TextField('IP adresas:', validators=[validators.required()])
    ports = TextField('Portai:')
    password = TextField('Slaptazodis:')
    internal = TextField('Vidinis IP adresas:')

