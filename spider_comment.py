# !/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@Author  : Sprite
@File    : spider_comment.py
@Time    : 2020/10/27 0027 8:39
@Program : Pycharm
'''

#  爬取电影短评

from bs4 import BeautifulSoup        #网页解析
import re                            #正则表达式，进行文字匹配
import urllib.request,urllib.error   #制定url，获取网页数据

import sqlite3                       #进行sqlite数据库操作

import time                          # 设置延时执行程序

#  查找评论人的名称
findUser = re.compile(r'<a class="" href="https://www.douban.com/people/.*/">(.*)</a>')

#  查找评分等级
findRating = re.compile(r'<span class="allstar(\d)')

# 查找评论内容
findWord = re.compile(r'<span class="short">(.*)</span>')




def main():

    dbpath = 'movie.db'
    conn = sqlite3.connect(dbpath)

    # 存储电影对应的url信息
    datalist = []

    sql = '''
    select link from movie '''

    c = conn.cursor()  # 获取游标
    data = c.execute(sql)  # 执行sql语句
    for item in data:
        datalist.append(item)


    # print(datalist[0])

    link1 = datalist[0]

    # print(link1)

    datalist = getComment(datalist,dbpath)
    #
    marklist = []
    for data in datalist:
        for i in range(len(data)):
            if(type(data[i]).__name__ == 'list'):
                data[i] = ''.join(data[i])

        marklist.append(data)

    comment = marklist

    saveData2DB(comment,dbpath)


def saveData2DB(comment, dbpath):
    # init_db(dbpath)

    conn = sqlite3.connect(dbpath)
    c = conn.cursor()  # 获取游标

    # print(comment)

    for data in comment:
            for j in range(len(data)):
                data[j] = data[j].replace('"','')
                data[j] = data[j].replace("'","")
                data[j] = '"' + data[j] + '"'
                sql = '''
                insert into comment(
                user,rating,word,movie_name)
                values(%s)''' % ",".join(data)
            c.execute(sql)
            conn.commit()


    print("插入数据成功")
    c.close()
    conn.close()



def init_db(dbpath):
    sql='''
    create table comment(
    id integer primary key autoincrement,
    user text,
    rating varchar,
    word text,
    movie_name text
    )
    '''  # 创建数据库

    conn = sqlite3.connect(dbpath)

    c = conn.cursor()  # 获取游标
    c.execute(sql)   # 执行sql语句
    conn.commit()  # 提交数据库操作
    conn.close()  # 关闭数据库连接

def getComment(datalist,dbpath):
    comment = []
    for i in range(16,30):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()  # 获取游标
        baseurl = datalist[i]
        link1 = baseurl
    # print(link1)
        baseurl = baseurl[0]
        print(baseurl)
        sql = '''select name from movie
        where link = ?'''
        name = c.execute(sql, (link1))
        namelist = []
        for item in name:
            namelist.append(item)
            name = namelist[0][0]
            print(name)

        baseurl = baseurl + 'comments?start='
        # print(baseurl)
        url1 = '&status=P&sort=new_score'

        for i in range(0, 5):
            url = baseurl + str(i * 20) + url1
            html = askURL(url)
            # print(html)

            # 逐一解析数据

            soup = BeautifulSoup(html, 'html.parser')
            # 查找符合要求的字符串，形成列表
            for item in soup.find_all('div', class_="comment"):
                data = []  # 保存一条评论的所有信息
                item = str(item)
                # print(item)
                #  存储用户名

                user = re.findall(findUser, item)
                if len(user) != 0:
                    user = user[0]
                    data.append(user)
                else:
                    data.append('')
                #  存储评分
                rating = re.findall(findRating, item)
                if (len(rating) != 0):
                    rating = rating[0]
                    data.append(rating)
                else:
                    data.append(rating)

                #  存储评论内容
                word = re.findall(findWord, item)
                if len(word) != 0:
                    word = word[0]
                    data.append(word)
                else:
                    data.append('')
                # 存储对应的电影名
                data.append(name)

                # 将一条评论所有信息存入comment
                comment.append(data)
            time.sleep(1)


        time.sleep(5)




    #
        print(len(comment))
    #
    conn.commit()  # 提交数据库操作
    conn.close()  # 关闭数据库连接
    #
    #
    # print(comment)
    return comment


def askURL(url):
    # 用户代理，表示告诉豆瓣浏览器，我们是什么类型的浏览器
    # 模拟浏览器头部，向豆瓣发送消息

    # proxy = {
    #     'http': 'http://218.66.253.146:8800'
    # }

    # params = {
    #     'wd': 'ip地址'
    # }


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


if __name__ == "__main__":     # 当程序执行时
    main()