import pymysql
import pandas
import os


def mysql_preset():

    db = pymysql.connect(host='localhost', user='root', password='121031', charset='UTF8MB4')
    cur = db.cursor()
    try:
        cur.execute('create database Student_info character set UTF8MB4;')
    except pymysql.err.ProgrammingError:
        pass
    cur.execute('use Student_info;')
    try:
        cur.execute('create table students\
        (学号 varchar(30),\
        姓名 varchar(30),\
        性别 varchar(30),\
        专业 varchar(30))\
        character set UTF8MB4;')
    except pymysql.err.InternalError:
        pass
    try:
        cur.execute('create table courses\
        (课程号 varchar(30),\
        课程名 varchar(30),\
        开课专业 varchar(30))\
        character set UTF8MB4;')
    except pymysql.err.InternalError:
        pass
    try:
        cur.execute('create table majors\
        (专业名称 varchar(30),\
        学生数 varchar(30),\
        课程数 varchar(30))\
        character set UTF8MB4;')
    except pymysql.err.InternalError:
        pass
    try:
        cur.execute('create table scores\
        (学号 varchar(30),\
        课程号 varchar(30),\
        分数 varchar(30))\
        character set UTF8MB4;')
    except pymysql.err.InternalError:
        pass
    db.commit()
    cur.close()
    db.close()


def user_write_preset():

    file_list = os.listdir()
    if '系统用户注册信息.xlsx' not in file_list:
        file = pandas.DataFrame({'登录名':['root'], '用户类型':['管理员'], '密码': ['121031']})
        title = ['登录名', '用户类型', '密码']
        file.to_excel('系统用户注册信息.xlsx', index=False ,columns=title)