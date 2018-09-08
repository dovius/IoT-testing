#!/usr/bin/python

import sys
import requests
import MySQLdb
import time

db = MySQLdb.connect(host="db", user='root', db="NVR")
cursor = db.cursor()


# mongoClient = MongoClient('localhost', 27017)
# mongoDb = mongoClient['iot-app']


# collection = db['nvrCollection']

def refresh():
    sqlSelect = 'SELECT ip FROM NVR'
    cursor.execute(sqlSelect)
    results = cursor.fetchall()
    ipList = [result[0] for result in results]

    f = open('NVR.txt', 'r')
    for line in f:
        ip, name = line.split(',')
        name = name.replace('\n', '')
        if ip not in ipList:
            try:
                print name + ' -> new device found'
                nowDate = time.strftime('%Y-%m-%d')
                nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    'INSERT INTO NVR (ip, name, add_date, off_until_date, on_until_date) VALUES (%s, %s, %s, %s, %s)', \
                    (ip, name, nowDate, nowTime, '2010-01-01 01:01:01'))
                db.commit()
            except:
                print 'db error on init'
                db.rollback()


# def mongoRefresh():
#     ipList = list(mongoDb.nvrCollection.find({}, {"ip": 1}))
#     f = open('NVR.txt', 'r')
#     for line in f:
#         ip, name = line.split(',')
#         name = name.replace('\n', '')
#         if ip not in ipList:
#             try:
#                 print name + ' -> new device found'
#                 nowDate = time.strftime('%Y-%m-%d')
#                 nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
#                 mongoDb.nvrCollection.insert({
#                     'ip': ip,
#                     'name': name,
#                     'add_date': nowDate,
#                     'off_until_date': nowTime,
#                     'on_until_date': '2010-01-01 01:01:01'
#                 })
#             except:
#                 print 'db error on init'
#                 db.rollback()


def setup():
    sql = """CREATE TABLE NVR (
            id INT NOT NULL AUTO_INCREMENT,
            ip VARCHAR(20),
            name VARCHAR(40),
            add_date DATE,
            on_until_date DATETIME,
            off_until_date DATETIME,
            PRIMARY KEY (id))"""

    sql2 = """CREATE TABLE EVENT (
            id INT NOT NULL,
            time DATETIME,
            status TINYINT(1))"""

    sql3 = """CREATE TABLE CONF (
            time DATETIME)"""

    cursor.execute('DROP TABLE IF EXISTS NVR')
    cursor.execute('DROP TABLE IF EXISTS EVENT')
    cursor.execute('DROP TABLE IF EXISTS CONF')
    cursor.execute(sql)
    cursor.execute(sql2)
    cursor.execute(sql3)
    cursor.execute('insert into CONF (time) VALUES (NOW())')

    # mongo
    # mongoDb.nvrCollection.drop()
    # mongoDb.eventCollection.drop()
    # mongoDb.confCollection.drop()
    # mongoDb.confCollection.insert({'time': time.strftime('%Y-%m-%d %H:%M:%S')})


def mysqlScan():
    sqlSelect2 = 'SELECT * FROM NVR'
    cursor.execute(sqlSelect2)
    results = cursor.fetchall()

    for row in results:
        ip = row[1]
        name = row[2]
        dateOnUntil = row[4]
        dateOffUntil = row[5]
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        nowDate = time.strftime('%Y-%m-%d')

        if dateOnUntil is None:
            dateOnUntil = 'NULL'
        if dateOffUntil is None:
            dateOffUntil = 'NULL'

        try:
            r = requests.get('http://' + ip, verify=False, timeout=3)
            print name + ' -> ' + 'Connected'
            status = True
        except:
            print name + ' -> ' + ' -'
            status = False
        try:
            if status == True:
                if dateOnUntil <= dateOffUntil:
                    cursor.execute('UPDATE NVR SET on_until_date=%s WHERE id=%s', \
                                   (nowTime, row[0]))
                    cursor.execute('INSERT INTO EVENT (id, time, status) VALUES (%s, %s, %s)', \
                                   (row[0], nowTime, status))
            else:
                if dateOnUntil >= dateOffUntil:
                    cursor.execute('UPDATE NVR SET off_until_date=%s WHERE id=%s', \
                                   (nowTime, row[0]))
                    cursor.execute('INSERT INTO EVENT (id, time, status) VALUES (%s, %s, %s)', \
                                   (row[0], nowTime, status))
            db.commit()
        except MySQLdb.Error, e:
            print str(e)
            db.rollback()

    cursor.execute('update CONF set time = NOW() LIMIT 1')
    db.commit()


# def mongoScan():
#     results = list(mongoDb.nvrCollection.find({}))
#     for row in results:
#         id = row['_id']
#         ip = row['ip']
#         name = row['name']
#         dateOnUntil = row['add_date']
#         dateOffUntil = row['off_until_date']
#         dateOnUntil = row['on_until_date']
#         nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
#         nowDate = time.strftime('%Y-%m-%d')
#
#         if dateOnUntil is None:
#             dateOnUntil = 'NULL'
#         if dateOffUntil is None:
#             dateOffUntil = 'NULL'
#
#         try:
#             r = requests.get('http://' + ip, verify=False, timeout=3)
#             print name + ' -> ' + 'Connected'
#             status = True
#         except:
#             print name + ' -> ' + ' -'
#             status = False
#         try:
#             if status == True:
#                 if dateOnUntil <= dateOffUntil:
#                     mongoDb.nvrCollection.update({
#                         '_id': id
#                     }, {
#                         '$set': {
#                             'on_until_date': nowTime
#                         }
#                     })
#
#                     mongoDb.eventCollection.insert({
#                         '_id': id,
#                         'time': nowTime,
#                         'status': status
#                     })
#             else:
#                 if dateOnUntil >= dateOffUntil:
#
#                     mongoDb.nvrCollection.update({
#                         '_id': id
#                     }, {
#                         '$set': {
#                             'off_until_date': nowTime
#                         }
#                     })
#
#                     mongoDb.eventCollection.insert({
#                         '_id': id,
#                         'time': nowTime,
#                         'status': status
#                     })
#         except MySQLdb.Error, e:
#             print str(e)
#
#     mongoDb.confCollection.update({}, {'$set': {'time': time.strftime('%Y-%m-%d %H:%M:%S')}})

for arg in sys.argv:
    if arg == 'refresh':
        refresh()
        # mongoRefresh()
    if arg == 'setup':
        setup()
        refresh()
        # mongoRefresh()

mysqlScan()
# mongoScan()
