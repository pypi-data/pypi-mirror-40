# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb
from selenium import webdriver
import time
import re
import requests
import os
import datetime


conn = MySQLdb.connect(host = '47.93.243.251',  # 远程主机的ip地址，
                                            user = 'root',   # MySQL用户名
                                            db = 'mini',   # database名
                                            passwd = 'GZhthb2017@sql',   # 数据库密码
                                            port = 33060,  #数据库监听端口，默认3306
                                            charset = "utf8")

nowNow = time.strftime("%Y%m%d%H%M%S", time.localtime())
cityPath = ur'E:\work\try\improcity'
countryPath = ur'E:\work\try\country'

today=datetime.date.today()
print today
formattedToday=today.strftime('%y%m%d')

def main(path):
    lis = []  # 放置文本信息和图片的绝对路径
    title = None
    cate = path.split('\\')[-1]
    if cate == 'improcity':
        category = '重点城市'
    if cate == 'country':
        category = '全国'
    localPath = os.path.join(path, formattedToday)
    if not os.path.exists(localPath):
        print('没有数据！！！')
    else:
        titlePath = os.path.join(localPath, 'title.txt')
        try:
            with open(titlePath, 'r') as f:
                title = f.read()
        except:
            print("没有title.txt")
        picsPath = os.path.join(localPath, 'pics')
        try:
            for dirpath, dirnames, filenames in os.walk(picsPath):
                for file in filenames:
                    p = os.path.join(picsPath, file)
                    print(p)
                    lis.append(p)
        except:
            print('图片路径存储有问题')
    nowNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    cursor = conn.cursor()
    pics_path = ','.join(lis)
    sql = 'insert into weibo_article(id, gzhname, category, title, newslink, pics_path, create_time,png_times) values (NULL, u"weibo", %s, %s, NULL , %s,%s, null)'
    try:
        cursor.execute(sql, (category, title, pics_path, nowNow))
        conn.commit()
        print('添加成功！！')
    except:
        conn.rollback()

    return title, lis


main(cityPath)
main(countryPath)
conn.close()
