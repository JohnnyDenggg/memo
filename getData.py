import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *

def checkDB():
    # 创建数据库
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('./db/database.db')
    if not db.open():
        print('无法建立与数据库的链接')
        return False

    # 检查todo表是否存在，不存在则创建表
    query = QSqlQuery()
    query.exec('create table todo(taskname varchar(10),status bool,details varchar(50))')
    # query.exec('insert into todo values("这是要做的事",False,"打发大水发大神大师傅大神范德萨发是打发大是否大师傅深度发的的所得税法地方萨芬的")')
    # query.exec('insert into todo values("事情二",True,"啥第三方大师傅")')

    # 检查todo表是否存在，不存在则创建表
    query.exec('create table done(taskname varchar(10),status bool,details varchar(50))')
    # query.exec('insert into done values("事情二",True,"已完成")')
    db.close()

def getTodoData():

    # 创建数据库
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('./db/database.db')
    if not db.open():
        print('无法建立与数据库的链接')
        return False

    # 检查表是否存在，不存在则创建表
    query = QSqlQuery()
    # 如果没有此表，则创建表
    query.exec('create table todo(taskname varchar(10),status varchar(50))')
    # query.exec('insert into todo values("这是要做的事","未完成")')
    # db.close()
    q = QSqlQuery()
    sql = 'select taskname,status,details from todo'
    q.exec(sql)
    data = []
    i = 0
    while q.next():

        taskname = q.value(0)
        status = q.value(1)
        details = q.value(2)
        data.append({'taskname': taskname, 'status': status,'details':details})
        i += 1
    print(data,i)
    db.close()
    return data,i



