#!/usr/bin/python

import sys
import requests
import MySQLdb
import time
import socket
import datetime

db = MySQLdb.connect(host="db", user='root', db="NVR", port=3306)
cursor = db.cursor()


# mongoClient = MongoClient('localhost', 27017)
# mongoDb = mongoClient['iot-app']
# collection = db['nvrCollection']

def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.settimeout(3)
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False


def is200(ip, port):
   try:
       r = requests.get('http://' + ip, timeout=(3, 3))
       if r.status_code == 200:
           return True
       return False
   except Exception:
       return False


def refresh():
    sqlSelect = 'SELECT ip FROM NVR'
    cursor.execute(sqlSelect)
    results = cursor.fetchall()
    ipList = [result[0] for result in results]

    f = open('app/NVR.txt', 'r')
    for line in f:
        ip, name, ports, password, internal, = line.split(',')
        name = name.replace('\n', '')
        if ip not in ipList:
            try:
                print name + ' -> new device found'
                nowDate = time.strftime('%Y-%m-%d')
                nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    'INSERT INTO NVR (ip, name, add_date, off_until_date, on_until_date, ports, password, internal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', \
                    (ip, name, nowDate, nowTime, '2010-01-01 01:01:01', ports, password, internal))
                db.commit()
            except MySQLdb.Error, e:
                print str(e)
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

        retryTimes = 1
        status = False
        if dateOnUntil > dateOffUntil:
            retryTimes = 6

        for i in range(retryTimes):
            print '[' + str(datetime.datetime.now()) + '] ' + name + ' ',
            is200resp = is200(ip, 80)
            isOpenResp = isOpen(ip, 8000)
            status = status or is200resp or isOpenResp
            if is200resp:
                print '80',
            if isOpenResp:
                print '8000',
            print ' '
            if status:
                break
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


def backupData():
    backup = open('../../backup.txt', 'w+')
    # backup = open('backup.txt', 'w+')

    cursor.execute('SELECT * FROM NVR')
    nvrs = cursor.fetchall()
    for nvr in nvrs:
        backup.write(nvr[1] + ',' + nvr[2] + ',' + nvr[6] + ',' + nvr[7] + ',' + nvr[8])
        if not nvr[8].endswith('\n'):
            backup.write('\n')
    backup.close()

for arg in sys.argv:
    if arg == 'refresh':
        refresh()
        # mongoRefresh()
    if arg == 'setup':
        setup()
        refresh()
        # mongoRefresh()

backupData()

mysqlScan()
# mongoScan()

db.close()