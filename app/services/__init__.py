import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user='root', db="NVR", port=32000)
cursor = db.cursor()