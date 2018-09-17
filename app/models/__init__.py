import MySQLdb
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

db = MySQLdb.connect(host="db", user='root', db="NVR", port=3306)
cursor = db.cursor()

class ReusableForm(Form):
    name = TextField('Pavadinimas:', validators=[validators.required()])
    ipAddress = TextField('IP adresas:', validators=[validators.required()])
    ports = TextField('Portai:')
    password = TextField('Slaptazodis:')
    internal = TextField('Vidinis IP adresas:')

