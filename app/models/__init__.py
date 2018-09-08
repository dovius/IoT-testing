import MySQLdb
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

db = MySQLdb.connect(host="127.0.0.1", user='root', db="NVR", port=32000)
cursor = db.cursor()

class ReusableForm(Form):
    name = TextField('Pavadinimas:', validators=[validators.required()])
    ipAddress = TextField('IP adresas:', validators=[validators.required()])