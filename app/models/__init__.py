import MySQLdb

db = MySQLdb.connect(host="db", user='root', db="NVR")
cursor = db.cursor()