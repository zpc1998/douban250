# !/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Author  : Sprite
@File    : spider.py
@Time    : 2020/10/26 0026 15:01
@Program : Pycharm
'''

#  爬取电影信息

from bs4 import BeautifulSoup        #网页解析
import re                            #正则表达式，进行文字匹配
import urllib.request,urllib.error   #制定url，获取网页数据

import sqlite3                       #进行sqlite数据库操作
import json



def saveData2DB(data, dbpath):
    # init_db(dbpath)

    conn = sqlite3.connect(dbpath)
    c = conn.cursor()  # 获取游标

    for datalist in data:
        for mark in datalist:
            for j in range(len(mark)):
                mark[j] = '"' + mark[j] + '"'
                sql = '''
                insert into movie(
                name,director,link,rate,actors,img_link)
                values(%s)''' % ",".join(mark)
            c.execute(sql)
            conn.commit()
    c.close()
    conn.close()


def main():

    baseurl = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start="
    # 爬取网页
    # askURL(url)

    data = []
    
    dbpath = "movie_shuju.db"

    # 获取电影基本信息
    for i in range(20,30):
        datalist = getData(baseurl,i)
        data.append(datalist)

    # print(len(data))

    # print(data[0])

    # for datalist in data:
    #     for mark in datalist:
    #         for j in range(len(mark)):
    #             mark[j] = '"'+mark[j]+'"'



    # savepath = '豆瓣电影Top250.xls'
    dbpath = "movie.db"
    # 保存数据
    # saveData(datalist, savepath)

    saveData2DB(data, dbpath)

    print("成功")



    # showdata(dbpath)


def askURL(url):
    # 用户代理，表示告诉豆瓣浏览器，我们是什么类型的浏览器
    # 模拟浏览器头部，向豆瓣发送消息
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""

    try:
            response = urllib.request.urlopen(request)
            html = response.read().decode("utf-8")
            # print(html)
    except urllib.error.URLError as e:
            if hasattr(e, "code"):

               print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)


    return html

def getData(baseurl,i):
    datalist = []
    url = "&year_range=2010,2019"
    url = baseurl+str(i*20)+url
    data = askURL(url)

    # 将获取到的数据转换成字典
    data1 = json.loads(data)
    # print(type(data1))

    # 获取所有电影信息
    data = list(data1.values())
    data = data[0]


    for j in range(0,20):
        data2 = []
        title = str(data[j]['title'])
        data2.append(title)
        # print(title)

        # 存储电影导演
        director = data[j]['directors']
        director = director[0]
        data2.append(director)

        # 存储电影详情链接
        link = str(data[j]['url'])
        data2.append(link)

        # 存储电影评分
        rate = str(data[j]['rate'])
        data2.append(rate)

        # 存储电影主演名单
        actors = data[j]['casts']
        actor = ','.join(actors)
        data2.append(actor)

        # 存储电影封面链接
        img_link = str(data[j]['cover'])
        data2.append(img_link)

        # 将整部电影信息保存到datalist中
        datalist.append(data2)

        # print('1')





        # print(data)

    print('1')
    return datalist

def getData1(baseurl):
    datalist = []
    url = "&year_range=2010,2019"
    for i in range(1,2):
        url = baseurl+str(i*20)+url
        data = askURL(url)

        # 将获取到的数据转换成字典
        data1 = json.loads(data)
        # print(type(data1))

        # 获取所有电影信息
        data = list(data1.values())
        data = data[0]


        for i in range(0,20):
            # 存储电影名称
            data2 = []
            title = str(data[i]['title'])
            data2.append(title)

            # print(title)

            # 存储电影导演
            director = data[i]['directors']
            director = director[0]
            data2.append(director)

            # 存储电影详情链接
            link = str(data[i]['url'])
            data2.append(link)

            # 存储电影评分
            rate = str(data[i]['rate'])
            data2.append(rate)

            # 存储电影主演名单
            actors = data[i]['casts']
            # actor = ''
            # for j in (range(0,len(actors))):
            #     actor = actors[j]+actor
            data2.append(actors)

            # 存储电影封面链接
            img_link = str(data[i]['cover'])
            data2.append(img_link)

            # 将整部电影信息保存到datalist中
            datalist.append(data2)



        # print(data)

    print(len(datalist))
    return datalist


def init_db(dbpath):
    sql='''
    create table movie(
    id integer primary key autoincrement,
    name text,
    director varchar,
    link text,
    rate numeric,
    actors text,
    img_link text
    )
    '''  # 创建数据库

    conn = sqlite3.connect(dbpath)

    c = conn.cursor()  # 获取游标
    c.execute(sql)   # 执行sql语句
    conn.commit()  # 提交数据库操作
    conn.close()  # 关闭数据库连接




if __name__ == "__main__":     # 当程序执行时
    main()