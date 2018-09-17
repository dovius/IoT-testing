import MySQLdb

db = MySQLdb.connect(host="db", user='root', db="NVR", port=3306)
cursor = db.cursor()